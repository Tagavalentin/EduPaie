from PySide6.QtCore import QAbstractTableModel, Qt
from typing import List, Any

from src.utils.formatters import format_fcfa


class StudentsTableModel(QAbstractTableModel):
    """Modèle de tableau pour la liste des élèves."""
    
    COLUMNS = ["Nom", "Prénom", "Classe", "Année", "Total dû", "Payé", "Solde", "Statut"]
    
    def __init__(self, students_data: List[dict], parent=None):
        super().__init__(parent)
        self.students_data = students_data
    
    def rowCount(self, parent=None) -> int:
        return len(self.students_data)
    
    def columnCount(self, parent=None) -> int:
        return len(self.COLUMNS)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            student_data = self.students_data[row]
            student = student_data['student']
            
            if col == 0:  # Nom
                return student.nom
            elif col == 1:  # Prénom
                return student.prenom
            elif col == 2:  # Classe
                return student.classe
            elif col == 3:  # Année
                return student.annee_scolaire
            elif col == 4:  # Total dû
                return format_fcfa(student.total_du)
            elif col == 5:  # Payé
                return format_fcfa(student_data['total_paid'])
            elif col == 6:  # Solde
                return format_fcfa(student_data['balance'])
            elif col == 7:  # Statut
                return student_data['status'].value
        
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section]
        return None
