from PySide6.QtCore import QAbstractTableModel, Qt
from typing import List, Any

from src.utils.formatters import format_fcfa, format_payment_mode


class PaymentsTableModel(QAbstractTableModel):
    """Modèle de tableau pour l'historique des paiements."""
    
    COLUMNS = ["Date", "Montant", "Mode", "N° Reçu", "Solde après"]
    
    def __init__(self, payments: List, parent=None):
        super().__init__(parent)
        self.payments = payments
    
    def rowCount(self, parent=None) -> int:
        return len(self.payments)
    
    def columnCount(self, parent=None) -> int:
        return len(self.COLUMNS)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            payment = self.payments[row]
            
            if col == 0:  # Date
                return payment.date_paiement
            elif col == 1:  # Montant
                return format_fcfa(payment.montant)
            elif col == 2:  # Mode
                # Formater le mode de paiement
                return format_payment_mode(payment.mode_paiement)
            elif col == 3:  # Numéro de reçu
                return payment.numero_recu
            elif col == 4:  # Solde après
                return format_fcfa(payment.solde_apres)
        
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section]
        return None
