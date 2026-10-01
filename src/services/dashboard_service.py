from typing import List, Dict

from src.repositories.student_repository import StudentRepository
from src.repositories.payment_repository import PaymentRepository
from src.services.student_service import StudentService, PaymentStatus


class DashboardService:
    """Service pour les statistiques du tableau de bord."""
    
    def __init__(self):
        self.student_repo = StudentRepository()
        self.payment_repo = PaymentRepository()
        self.student_service = StudentService()
    
    def get_statistics(self) -> Dict:
        """
        Calcule les statistiques globales.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        students = self.student_repo.get_all()
        
        total_students = len(students)
        total_due = sum(s.total_du for s in students)
        
        # Calculer le total encaissé
        total_paid = 0
        for student in students:
            total_paid += self.payment_repo.get_sum_by_student(student.id)
        
        # Calculer le total restant
        total_remaining = total_due - total_paid
        
        # Compter les élèves par statut
        paid_count = 0
        partial_count = 0
        unpaid_count = 0
        
        for student in students:
            status = self.student_service.get_payment_status(student.id)
            if status == PaymentStatus.PAID:
                paid_count += 1
            elif status == PaymentStatus.PARTIAL:
                partial_count += 1
            else:
                unpaid_count += 1
        
        return {
            'total_students': total_students,
            'total_due': total_due,
            'total_paid': total_paid,
            'total_remaining': total_remaining,
            'paid_count': paid_count,
            'partial_count': partial_count,
            'unpaid_count': unpaid_count,
            'unpaid_students_count': paid_count + partial_count  # Élèves non soldés
        }
    
    def get_students_by_status(self, status: PaymentStatus) -> List[Dict]:
        """
        Récupère les élèves filtrés par statut.
        
        Args:
            status: Le statut de paiement
            
        Returns:
            Liste des élèves avec leurs informations
        """
        all_students = self.student_service.get_all_students_with_status()
        
        return [s for s in all_students if s['status'] == status]
