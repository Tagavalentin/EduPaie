from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QSpinBox, QDateEdit, QComboBox, QPushButton, 
                                 QMessageBox, QGroupBox, QCheckBox)
from PySide6.QtCore import Qt, QDate
import subprocess
import platform

from src.services.payment_service import PaymentService
from src.services.student_service import StudentService
from src.utils.formatters import format_fcfa
from src.utils.pdf_generator import PDFGenerator


class PaymentDialog(QDialog):
    """Dialogue d'enregistrement d'un paiement."""
    
    def __init__(self, parent=None, student_id: int = None):
        super().__init__(parent)
        self.student_id = student_id
        self.payment_service = PaymentService()
        self.student_service = StudentService()
        
        self.setWindowTitle("Enregistrer un paiement")
        self.setMinimumWidth(500)
        
        self._setup_ui()
        self._load_student_info()
    
    def _setup_ui(self):
        """Configure l'interface du dialogue."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Informations de l'élève
        self.student_info_group = QGroupBox("Informations de l'élève")
        student_layout = QVBoxLayout(self.student_info_group)
        
        self.student_name_label = QLabel("Chargement...")
        self.student_name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        student_layout.addWidget(self.student_name_label)
        
        self.balance_label = QLabel("Solde: ")
        self.balance_label.setStyleSheet("font-size: 16px; color: #e74c3c;")
        student_layout.addWidget(self.balance_label)
        
        layout.addWidget(self.student_info_group)
        
        # Formulaire de paiement
        form_group = QGroupBox("Détails du paiement")
        form_layout = QVBoxLayout(form_group)
        
        # Montant
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Montant (FCFA) *:")
        amount_label.setFixedWidth(150)
        self.amount_input = QSpinBox()
        self.amount_input.setRange(1, 999999999)
        self.amount_input.setSingleStep(5000)
        self.amount_input.setSuffix(" FCFA")
        self.amount_input.valueChanged.connect(self._on_amount_changed)
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        form_layout.addLayout(amount_layout)
        
        # Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Date du paiement *:")
        date_label.setFixedWidth(150)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        form_layout.addLayout(date_layout)
        
        # Mode de paiement
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode de paiement *:")
        mode_label.setFixedWidth(150)
        self.mode_input = QComboBox()
        self.mode_input.addItems(["Espèces", "Chèque", "Virement", "Mobile Money"])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_input)
        form_layout.addLayout(mode_layout)
        
        # Générer le reçu
        self.generate_receipt_checkbox = QCheckBox("Générer le reçu PDF")
        self.generate_receipt_checkbox.setChecked(True)
        form_layout.addWidget(self.generate_receipt_checkbox)
        
        layout.addWidget(form_group)
        
        # Solde après paiement
        self.balance_after_label = QLabel("Solde après paiement: ")
        self.balance_after_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.balance_after_label)
        
        layout.addStretch()
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self.btn_cancel)
        
        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self._on_save)
        self.btn_save.setDefault(True)
        buttons_layout.addWidget(self.btn_save)
        
        layout.addLayout(buttons_layout)
    
    def _load_student_info(self):
        """Charge les informations de l'élève."""
        if not self.student_id:
            return
        
        from src.repositories.student_repository import StudentRepository
        repo = StudentRepository()
        student = repo.get_by_id(self.student_id)
        
        if student:
            self.student_name_label.setText(f"{student.nom} {student.prenom} - {student.classe}")
            
            balance = self.student_service.calculate_balance(self.student_id)
            self.balance_label.setText(f"Solde restant: {format_fcfa(balance)}")
            
            # Définir le montant maximum
            self.amount_input.setMaximum(balance)
            
            # Mettre à jour le solde après
            self._on_amount_changed()
    
    def _on_amount_changed(self):
        """Met à jour l'affichage du solde après paiement."""
        if not self.student_id:
            return
        
        balance = self.student_service.calculate_balance(self.student_id)
        amount = self.amount_input.value()
        
        balance_after = balance - amount
        self.balance_after_label.setText(f"Solde après paiement: {format_fcfa(balance_after)}")
        
        # Couleur selon le statut
        if balance_after == 0:
            self.balance_after_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #27ae60;")
        elif balance_after > 0:
            self.balance_after_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e67e22;")
        else:
            self.balance_after_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
    
    def _validate(self):
        """Valide les champs du formulaire."""
        amount = self.amount_input.value()
        date = self.date_input.date().toString("yyyy-MM-dd")
        mode = self.mode_input.currentText().lower().replace(" ", "_")
        
        # Valider le montant
        is_valid, error_msg = self.payment_service.validate_payment_amount(amount, self.student_id)
        if not is_valid:
            return False, error_msg
        
        # Valider la date
        is_valid, error_msg = self.payment_service.validate_payment_date(date)
        if not is_valid:
            return False, error_msg
        
        return True, ""
    
    def _on_save(self):
        """Gère l'enregistrement du paiement."""
        is_valid, error_msg = self._validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Erreur de validation", error_msg)
            return
        
        amount = self.amount_input.value()
        date = self.date_input.date().toString("yyyy-MM-dd")
        mode = self.mode_input.currentText().lower().replace(" ", "_")
        
        # Confirmation
        balance = self.student_service.calculate_balance(self.student_id)
        balance_after = balance - amount
        
        reply = QMessageBox.question(
            self,
            "Confirmer le paiement",
            f"Voulez-vous vraiment enregistrer un paiement de {format_fcfa(amount)} ?\n\n"
            f"Solde avant: {format_fcfa(balance)}\n"
            f"Solde après: {format_fcfa(balance_after)}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            payment, error = self.payment_service.create_payment(
                student_id=self.student_id,
                amount=amount,
                date_paiement=date,
                mode_paiement=mode
            )
            
            if payment:
                # Générer le PDF si demandé
                if self.generate_receipt_checkbox.isChecked():
                    self._generate_receipt_pdf(payment)
                
                QMessageBox.information(
                    self,
                    "Paiement enregistré",
                    f"Paiement enregistré avec succès !\n\n"
                    f"Numéro de reçu: {payment.numero_recu}\n"
                    f"Montant: {format_fcfa(payment.montant)}\n"
                    f"Solde après: {format_fcfa(payment.solde_apres)}"
                )
                self.accept()
            else:
                QMessageBox.critical(self, "Erreur", error)
    
    def _generate_receipt_pdf(self, payment):
        """Génère et ouvre le reçu PDF."""
        from src.repositories.student_repository import StudentRepository
        repo = StudentRepository()
        student = repo.get_by_id(payment.student_id)
        
        if not student:
            return
        
        try:
            generator = PDFGenerator()
            from pathlib import Path
            output_path = Path.home() / "Desktop" / f"recu_{payment.numero_recu}.pdf"
            generator.generate_receipt(payment, student, output_path)
            
            # Ouvrir le PDF
            self._open_file(output_path)
            
        except Exception as e:
            QMessageBox.warning(self, "Avertissement", 
                               f"Le PDF n'a pas pu être généré : {str(e)}")
    
    def _open_file(self, file_path):
        """Ouvre un fichier avec l'application par défaut du système."""
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(['start', '', str(file_path)], shell=True)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', str(file_path)])
            else:  # Linux
                subprocess.Popen(['xdg-open', str(file_path)])
        except Exception as e:
            QMessageBox.warning(self, "Avertissement", 
                               f"Le fichier n'a pas pu être ouvert : {str(e)}")
