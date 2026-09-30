from typing import List, Optional
from enum import Enum

from src.repositories.student_repository import StudentRepository
from src.repositories.payment_repository import PaymentRepository
from src.models.student import Student


class PaymentStatus(Enum):
    """Statut de paiement d'un élève."""
    PAID = "Soldé"
    PARTIAL = "Partiellement payé"
    UNPAID = "Non payé"


class StudentService:
    """Service pour la logique métier liée aux élèves."""
    
    def __init__(self):
        self.student_repo = StudentRepository()
        self.payment_repo = PaymentRepository()
    
    def calculate_balance(self, student_id: int) -> int:
        """
        Calcule le solde restant d'un élève.
        
        Args:
            student_id: L'id de l'élève
            
        Returns:
            Le solde restant (0 si soldé)
        """
        student = self.student_repo.get_by_id(student_id)
        if not student:
            return 0
        
        total_paid = self.payment_repo.get_sum_by_student(student_id)
        return student.total_du - total_paid
    
    def get_payment_status(self, student_id: int) -> PaymentStatus:
        """
        Détermine le statut de paiement d'un élève.
        
        Args:
            student_id: L'id de l'élève
            
        Returns:
            Le statut de paiement
        """
        balance = self.calculate_balance(student_id)
        
        if balance == 0:
            return PaymentStatus.PAID
        elif balance > 0:
            return PaymentStatus.PARTIAL
        else:
            # Ne devrait pas arriver avec les contraintes, mais au cas où
            return PaymentStatus.UNPAID
    
    def get_student_with_status(self, student_id: int) -> Optional[dict]:
        """
        Récupère un élève avec son solde et son statut.
        
        Args:
            student_id: L'id de l'élève
            
        Returns:
            Dictionnaire avec les infos de l'élève, solde et statut, ou None
        """
        student = self.student_repo.get_by_id(student_id)
        if not student:
            return None
        
        balance = self.calculate_balance(student_id)
        status = self.get_payment_status(student_id)
        total_paid = self.payment_repo.get_sum_by_student(student_id)
        
        return {
            'student': student,
            'total_paid': total_paid,
            'balance': balance,
            'status': status
        }
    
    def get_all_students_with_status(self) -> List[dict]:
        """
        Récupère tous les élèves avec leur solde et statut.
        
        Returns:
            Liste de dictionnaires avec les infos de chaque élève
        """
        students = self.student_repo.get_all()
        result = []
        
        for student in students:
            balance = self.calculate_balance(student.id)
            status = self.get_payment_status(student.id)
            total_paid = self.payment_repo.get_sum_by_student(student.id)
            
            result.append({
                'student': student,
                'total_paid': total_paid,
                'balance': balance,
                'status': status
            })
        
        return result
    
    def can_delete_student(self, student_id: int) -> tuple[bool, str]:
        """
        Vérifie si un élève peut être supprimé.
        
        Args:
            student_id: L'id de l'élève
            
        Returns:
            Tuple (peut_supprimer, message_erreur)
        """
        if self.student_repo.has_payments(student_id):
            return False, "Impossible de supprimer cet élève car il a des paiements enregistrés."
        
        return True, ""
