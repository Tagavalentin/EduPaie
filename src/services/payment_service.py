import sqlite3
from datetime import datetime
from typing import Optional, Tuple

from src.repositories.student_repository import StudentRepository
from src.repositories.payment_repository import PaymentRepository
from src.database.connection import get_connection, close_connection
from src.models.payment import Payment


class PaymentService:
    """Service pour la logique métier liée aux paiements."""
    
    def __init__(self):
        self.student_repo = StudentRepository()
        self.payment_repo = PaymentRepository()
    
    def validate_payment_amount(self, amount: int, student_id: int) -> Tuple[bool, str]:
        """
        Valide le montant d'un paiement.
        
        Args:
            amount: Le montant à valider
            student_id: L'id de l'élève
            
        Returns:
            Tuple (valide, message_erreur)
        """
        # Vérifier que le montant est un entier positif
        if not isinstance(amount, int):
            return False, "Le montant doit être un nombre entier."
        
        if amount <= 0:
            return False, "Le montant doit être strictement positif."
        
        # Vérifier que le montant ne dépasse pas le solde restant
        from src.services.student_service import StudentService
        student_service = StudentService()
        balance = student_service.calculate_balance(student_id)
        
        if amount > balance:
            from src.utils.formatters import format_fcfa
            return False, f"Le montant saisi ({format_fcfa(amount)}) dépasse le solde restant ({format_fcfa(balance)})."
        
        return True, ""
    
    def validate_payment_date(self, date_str: str) -> Tuple[bool, str]:
        """
        Valide une date de paiement.
        
        Args:
            date_str: La date au format YYYY-MM-DD
            
        Returns:
            Tuple (valide, message_erreur)
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "La date doit être au format JJ/MM/AAAA."

    def validate_payment_mode(self, mode_paiement: str) -> Tuple[bool, str]:
        """Vérifie que le mode de paiement est pris en charge."""
        valid_modes = {"especes", "cheque", "virement", "mobile_money"}
        if not isinstance(mode_paiement, str) or mode_paiement.strip().lower() not in valid_modes:
            return False, "Mode invalide. Choisissez Espèces, Chèque, Virement ou Mobile Money."
        return True, ""
    
    def generate_receipt_number(self, year: int) -> str:
        """
        Génère un numéro de reçu unique pour l'année donnée.
        
        Args:
            year: L'année (ex: 2025)
            
        Returns:
            Le numéro de reçu (ex: REC-2025-000001)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Compter le nombre de reçus pour cette année
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM payments 
                WHERE numero_recu LIKE ?
                """,
                (f"REC-{year}-%",)
            )
            count = cursor.fetchone()[0]
            
            # Générer le numéro avec padding
            next_number = count + 1
            receipt_number = f"REC-{year}-{next_number:06d}"
            
            return receipt_number
        finally:
            close_connection(conn)
    
    def create_payment(self, student_id: int, amount: int, date_paiement: str, 
                      mode_paiement: str) -> Tuple[Optional[Payment], str]:
        """
        Crée un paiement avec validation et génération atomique du numéro de reçu.
        
        Args:
            student_id: L'id de l'élève
            amount: Le montant du paiement
            date_paiement: La date du paiement (YYYY-MM-DD)
            mode_paiement: Le mode de paiement
            
        Returns:
            Tuple (payment, message_erreur)
        """
        # Valider le montant
        is_valid, error_msg = self.validate_payment_amount(amount, student_id)
        if not is_valid:
            return None, error_msg
        
        # Valider la date
        is_valid, error_msg = self.validate_payment_date(date_paiement)
        if not is_valid:
            return None, error_msg
        
        is_valid, error_msg = self.validate_payment_mode(mode_paiement)
        if not is_valid:
            return None, error_msg

        mode_paiement = mode_paiement.strip().lower()
        
        # Calculer le solde après paiement
        from src.services.student_service import StudentService
        student_service = StudentService()
        balance_before = student_service.calculate_balance(student_id)
        solde_apres = balance_before - amount
        
        # Créer le paiement dans une transaction atomique
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Générer le numéro de reçu
            year = datetime.strptime(date_paiement, "%Y-%m-%d").year
            receipt_number = self.generate_receipt_number(year)
            
            # Insérer le paiement
            cursor.execute(
                """
                INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (student_id, amount, date_paiement, mode_paiement, receipt_number, solde_apres)
            )
            
            # Récupérer le paiement créé
            payment_id = cursor.lastrowid
            cursor.execute(
                """
                SELECT id, student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres, created_at
                FROM payments WHERE id = ?
                """,
                (payment_id,)
            )
            row = cursor.fetchone()
            
            conn.commit()
            
            payment = Payment(
                id=row['id'],
                student_id=row['student_id'],
                montant=row['montant'],
                date_paiement=row['date_paiement'],
                mode_paiement=row['mode_paiement'],
                numero_recu=row['numero_recu'],
                solde_apres=row['solde_apres'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
            )
            
            return payment, ""
            
        except Exception as e:
            conn.rollback()
            return None, f"Erreur lors de la création du paiement : {str(e)}"
        finally:
            close_connection(conn)
