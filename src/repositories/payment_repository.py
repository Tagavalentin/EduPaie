import sqlite3
from typing import List, Optional
from datetime import datetime

from src.database.connection import get_connection, close_connection
from src.models.payment import Payment


class PaymentRepository:
    """Repository pour les opérations CRUD sur les paiements."""
    
    def create(self, payment: Payment) -> Payment:
        """
        Crée un nouveau paiement dans la base de données.
        
        Args:
            payment: Le paiement à créer (id doit être None)
            
        Returns:
            Le paiement créé avec son id généré
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (payment.student_id, payment.montant, payment.date_paiement,
                 payment.mode_paiement, payment.numero_recu, payment.solde_apres)
            )
            conn.commit()
            payment.id = cursor.lastrowid
            return payment
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            close_connection(conn)
    
    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """
        Récupère un paiement par son id.
        
        Args:
            payment_id: L'id du paiement
            
        Returns:
            Le paiement trouvé ou None
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres, created_at
                FROM payments 
                WHERE id = ?
                """,
                (payment_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return Payment(
                    id=row['id'],
                    student_id=row['student_id'],
                    montant=row['montant'],
                    date_paiement=row['date_paiement'],
                    mode_paiement=row['mode_paiement'],
                    numero_recu=row['numero_recu'],
                    solde_apres=row['solde_apres'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                )
            return None
        finally:
            close_connection(conn)
    
    def get_by_receipt_number(self, numero_recu: str) -> Optional[Payment]:
        """
        Récupère un paiement par son numéro de reçu.
        
        Args:
            numero_recu: Le numéro de reçu
            
        Returns:
            Le paiement trouvé ou None
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres, created_at
                FROM payments 
                WHERE numero_recu = ?
                """,
                (numero_recu,)
            )
            row = cursor.fetchone()
            
            if row:
                return Payment(
                    id=row['id'],
                    student_id=row['student_id'],
                    montant=row['montant'],
                    date_paiement=row['date_paiement'],
                    mode_paiement=row['mode_paiement'],
                    numero_recu=row['numero_recu'],
                    solde_apres=row['solde_apres'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                )
            return None
        finally:
            close_connection(conn)
    
    def get_by_student(self, student_id: int) -> List[Payment]:
        """
        Récupère tous les paiements d'un élève.
        
        Args:
            student_id: L'id de l'élève
            
        Returns:
            La liste des paiements de l'élève (du plus récent au plus ancien)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres, created_at
                FROM payments 
                WHERE student_id = ?
                ORDER BY date_paiement DESC, created_at DESC
                """,
                (student_id,)
            )
            rows = cursor.fetchall()
            
            payments = []
            for row in rows:
                payments.append(Payment(
                    id=row['id'],
                    student_id=row['student_id'],
                    montant=row['montant'],
                    date_paiement=row['date_paiement'],
                    mode_paiement=row['mode_paiement'],
                    numero_recu=row['numero_recu'],
                    solde_apres=row['solde_apres'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                ))
            return payments
        finally:
            close_connection(conn)
    
    def get_all(self) -> List[Payment]:
        """
        Récupère tous les paiements.
        
        Returns:
            La liste de tous les paiements (du plus récent au plus ancien)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres, created_at
                FROM payments 
                ORDER BY date_paiement DESC, created_at DESC
                """
            )
            rows = cursor.fetchall()
            
            payments = []
            for row in rows:
                payments.append(Payment(
                    id=row['id'],
                    student_id=row['student_id'],
                    montant=row['montant'],
                    date_paiement=row['date_paiement'],
                    mode_paiement=row['mode_paiement'],
                    numero_recu=row['numero_recu'],
                    solde_apres=row['solde_apres'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                ))
            return payments
        finally:
            close_connection(conn)
    
    def get_sum_by_student(self, student_id: int) -> int:
        """
        Calcule la somme des paiements d'un élève.
        
        Args:
            student_id: L'id de l'élève
            
        Returns:
            La somme des paiements (0 si aucun paiement)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT COALESCE(SUM(montant), 0) FROM payments WHERE student_id = ?",
                (student_id,)
            )
            return cursor.fetchone()[0] or 0
        finally:
            close_connection(conn)
    
    def delete(self, payment_id: int) -> bool:
        """
        Supprime un paiement.
        
        Args:
            payment_id: L'id du paiement à supprimer
            
        Returns:
            True si supprimé, False si le paiement n'existe pas
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            close_connection(conn)
