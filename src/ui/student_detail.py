from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QPushButton, QTableView, QHeaderView, QMessageBox,
                                 QGroupBox, QDialog)
from PySide6.QtCore import Qt

from src.services.student_service import StudentService, PaymentStatus
from src.repositories.payment_repository import PaymentRepository
from src.utils.formatters import format_fcfa


class StudentDetail(QWidget):
    """Vue détaillée d'un élève avec historique des paiements."""
    
    def __init__(self, student_id: int, parent=None):
        super().__init__(parent)
        self.student_id = student_id
        self.student_service = StudentService()
        self.payment_repo = PaymentRepository()
        
        self._setup_ui()
        self._load_student_info()
    
    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Informations de l'élève
        info_group = QGroupBox("Informations de l'élève")
        info_layout = QVBoxLayout(info_group)
        
        self.name_label = QLabel()
        self.name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        info_layout.addWidget(self.name_label)
        
        self.class_label = QLabel()
        info_layout.addWidget(self.class_label)
        
        self.year_label = QLabel()
        info_layout.addWidget(self.year_label)
        
        layout.addWidget(info_group)
        
        # Situation financière
        finance_group = QGroupBox("Situation financière")
        finance_layout = QVBoxLayout(finance_group)
        
        # Total dû
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("Total dû:"))
        self.total_label = QLabel()
        self.total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()
        finance_layout.addLayout(total_layout)
        
        # Total payé
        paid_layout = QHBoxLayout()
        paid_layout.addWidget(QLabel("Total payé:"))
        self.paid_label = QLabel()
        self.paid_label.setStyleSheet("font-size: 16px; color: #27ae60; font-weight: bold;")
        paid_layout.addWidget(self.paid_label)
        paid_layout.addStretch()
        finance_layout.addLayout(paid_layout)
        
        # Solde
        balance_layout = QHBoxLayout()
        balance_layout.addWidget(QLabel("Solde restant:"))
        self.balance_label = QLabel()
        self.balance_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        balance_layout.addWidget(self.balance_label)
        balance_layout.addStretch()
        finance_layout.addLayout(balance_layout)
        
        # Statut
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Statut:"))
        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        finance_layout.addLayout(status_layout)
        
        layout.addWidget(finance_group)
        
        # Historique des paiements
        history_group = QGroupBox("Historique des paiements")
        history_layout = QVBoxLayout(history_group)
        
        self.payments_table = QTableView()
        self.payments_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.payments_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.payments_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.payments_table.doubleClicked.connect(self._on_double_click)
        
        header = self.payments_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        
        history_layout.addWidget(self.payments_table)
        
        # Bouton Revoir le reçu
        receipt_layout = QHBoxLayout()
        receipt_layout.addStretch()
        
        self.btn_receipt = QPushButton("Revoir le reçu")
        self.btn_receipt.clicked.connect(self._on_view_receipt)
        self.btn_receipt.setEnabled(False)
        receipt_layout.addWidget(self.btn_receipt)
        
        history_layout.addLayout(receipt_layout)
        
        layout.addWidget(history_group)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.btn_close = QPushButton("Fermer")
        self.btn_close.clicked.connect(self._on_close)
        buttons_layout.addWidget(self.btn_close)
        
        layout.addLayout(buttons_layout)
    
    def _load_student_info(self):
        """Charge les informations de l'élève."""
        from src.repositories.student_repository import StudentRepository
        repo = StudentRepository()
        student = repo.get_by_id(self.student_id)
        
        if not student:
            QMessageBox.critical(self, "Erreur", "Élève introuvable")
            return
        
        # Informations de base
        self.name_label.setText(f"{student.nom} {student.prenom}")
        self.class_label.setText(f"Classe: {student.classe}")
        self.year_label.setText(f"Année scolaire: {student.annee_scolaire}")
        
        # Situation financière
        student_data = self.student_service.get_student_with_status(self.student_id)
        
        self.total_label.setText(format_fcfa(student.total_du))
        self.paid_label.setText(format_fcfa(student_data['total_paid']))
        self.balance_label.setText(format_fcfa(student_data['balance']))
        self.status_label.setText(student_data['status'].value)
        
        # Couleur du statut
        if student_data['status'] == PaymentStatus.PAID:
            self.status_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #27ae60;")
            self.balance_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")
        elif student_data['status'] == PaymentStatus.PARTIAL:
            self.status_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e67e22;")
            self.balance_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #e67e22;")
        else:
            self.status_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e74c3c;")
            self.balance_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c;")
        
        # Historique des paiements
        self._load_payments()
    
    def _load_payments(self):
        """Charge l'historique des paiements."""
        payments = self.payment_repo.get_by_student(self.student_id)
        
        from src.ui.payments_table_model import PaymentsTableModel
        model = PaymentsTableModel(payments)
        self.payments_table.setModel(model)
        self.payments_table.resizeColumnsToContents()
        
        # Connecter le signal de sélection
        if self.payments_table.selectionModel():
            self.payments_table.selectionModel().selectionChanged.connect(self._on_payment_selection_changed)
    
    def _on_double_click(self, index):
        """Gère le double-clic sur un paiement."""
        row = index.row()
        
        from src.ui.payments_table_model import PaymentsTableModel
        model = self.payments_table.model()
        payment = model.payments[row]
        
        # Afficher les détails du paiement
        self._show_payment_details(payment)
    
    def _show_payment_details(self, payment):
        """Affiche les détails d'un paiement."""
        from src.repositories.student_repository import StudentRepository
        repo = StudentRepository()
        student = repo.get_by_id(payment.student_id)
        
        details = (
            f"Numéro de reçu: {payment.numero_recu}\n"
            f"Élève: {student.nom} {student.prenom}\n"
            f"Montant: {format_fcfa(payment.montant)}\n"
            f"Date: {payment.date_paiement}\n"
            f"Mode: {payment.mode_paiement}\n"
            f"Solde après: {format_fcfa(payment.solde_apres)}"
        )
        
        QMessageBox.information(self, "Détails du paiement", details)
    
    def _on_payment_selection_changed(self):
        """Gère le changement de sélection dans le tableau des paiements."""
        has_selection = self.payments_table.selectionModel().hasSelection()
        self.btn_receipt.setEnabled(has_selection)
    
    def _on_view_receipt(self):
        """Gère le clic sur le bouton Revoir le reçu."""
        selected_rows = self.payments_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        
        from src.ui.payments_table_model import PaymentsTableModel
        model = self.payments_table.model()
        payment = model.payments[row]
        
        # Pour l'instant, afficher les détails
        # La génération PDF sera implémentée dans la branche feature/recus-pdf
        self._show_payment_details(payment)
    
    def _on_close(self):
        """Gère le clic sur le bouton Fermer."""
        # Émettre un signal pour revenir à la liste
        self.parent().parent().stack.setCurrentWidget(self.parent().parent().students_view)
    
    def refresh(self):
        """Actualise les informations."""
        self._load_student_info()


class StudentDetailDialog(QDialog):
    """Dialogue affichant la fiche détaillée d'un élève."""
    
    def __init__(self, student_id: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fiche élève")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.detail = StudentDetail(student_id, self)
        layout.addWidget(self.detail)
