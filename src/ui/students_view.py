from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                                 QLineEdit, QComboBox, QTableView, QHeaderView, 
                                 QMessageBox, QMenu)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from src.services.student_service import StudentService, PaymentStatus
from src.utils.formatters import format_fcfa


class StudentsView(QWidget):
    """Vue pour la gestion des élèves."""
    
    # Signal émis quand on demande de voir les détails d'un élève
    student_selected = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.student_service = StudentService()
        self.current_students = []
        
        self._setup_ui()
        self._load_students()
    
    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(16)
        
        # Barre d'outils
        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)
        
        # Tableau des élèves
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        self.table.doubleClicked.connect(self._on_double_click)
        
        # Ajuster les colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical_header = self.table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical_header.setMinimumSectionSize(40)
        
        layout.addWidget(self.table, stretch=1)
        
        # Menu contextuel
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
    
    def _create_toolbar(self) -> QWidget:
        """Crée la barre d'outils."""
        toolbar = QWidget()
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(10)
        
        # Bouton Ajouter
        self.btn_add = QPushButton("Ajouter")
        self.btn_add.clicked.connect(self._on_add)
        layout.addWidget(self.btn_add)
        
        # Bouton Modifier
        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_edit.setEnabled(False)
        layout.addWidget(self.btn_edit)
        
        # Bouton Supprimer
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_delete.setEnabled(False)
        layout.addWidget(self.btn_delete)
        
        # Bouton Enregistrer paiement
        self.btn_payment = QPushButton("Enregistrer paiement")
        self.btn_payment.clicked.connect(self._on_payment)
        self.btn_payment.setEnabled(False)
        layout.addWidget(self.btn_payment)
        
        layout.addStretch()
        
        # Recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par nom ou prénom...")
        self.search_input.textChanged.connect(self._on_search)
        layout.addWidget(self.search_input)
        
        # Filtre par classe
        self.class_filter = QComboBox()
        self.class_filter.addItem("Toutes les classes")
        self.class_filter.currentTextChanged.connect(self._on_filter_changed)
        layout.addWidget(self.class_filter)
        
        # Bouton Actualiser
        self.btn_refresh = QPushButton("Actualiser")
        self.btn_refresh.clicked.connect(self._load_students)
        layout.addWidget(self.btn_refresh)
        
        return toolbar
    
    def _load_students(self):
        """Charge et affiche la liste des élèves."""
        self.current_students = self.student_service.get_all_students_with_status()
        self._update_table()
        self._update_class_filter()
    
    def _update_table(self):
        """Met à jour le tableau avec les données actuelles."""
        from src.ui.students_table_model import StudentsTableModel
        
        model = StudentsTableModel(self.current_students)
        self.table.setModel(model)
        
        # Connecter le signal de sélection
        selection_model = self.table.selectionModel()
        if selection_model:
            selection_model.selectionChanged.connect(self._on_selection_changed)
        
    
    def _update_class_filter(self):
        """Met à jour la liste des classes dans le filtre."""
        # Sauvegarder la sélection actuelle
        current_filter = self.class_filter.currentText()
        
        # Récupérer les classes uniques
        classes = set()
        for data in self.current_students:
            classes.add(data['student'].classe)
        
        # Mettre à jour le combo box
        self.class_filter.blockSignals(True)
        self.class_filter.clear()
        self.class_filter.addItem("Toutes les classes")
        for classe in sorted(classes):
            self.class_filter.addItem(classe)
        
        # Restaurer la sélection si possible
        index = self.class_filter.findText(current_filter)
        if index >= 0:
            self.class_filter.setCurrentIndex(index)
        else:
            self.class_filter.setCurrentIndex(0)
        
        self.class_filter.blockSignals(False)
    
    def _on_selection_changed(self):
        """Gère le changement de sélection dans le tableau."""
        has_selection = self.table.selectionModel().hasSelection()
        self.btn_edit.setEnabled(has_selection)
        self.btn_delete.setEnabled(has_selection)
        self.btn_payment.setEnabled(has_selection)
    
    def _on_add(self):
        """Gère le clic sur le bouton Ajouter."""
        from src.ui.student_form import StudentForm
        
        form = StudentForm(self)
        if form.exec():
            self._load_students()
    
    def _on_edit(self):
        """Gère le clic sur le bouton Modifier."""
        from src.ui.student_form import StudentForm
        
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        student_data = self.current_students[row]
        
        form = StudentForm(self, student_data['student'])
        if form.exec():
            self._load_students()
    
    def _on_delete(self):
        """Gère le clic sur le bouton Supprimer."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        student_data = self.current_students[row]
        student = student_data['student']
        
        # Vérifier si l'élève peut être supprimé
        can_delete, error_msg = self.student_service.can_delete_student(student.id)
        
        if not can_delete:
            QMessageBox.warning(self, "Suppression impossible", error_msg)
            return
        
        # Confirmation
        reply = QMessageBox.question(
            self,
            "Confirmer la suppression",
            f"Voulez-vous vraiment supprimer l'élève {student.nom} {student.prenom} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from src.repositories.student_repository import StudentRepository
            repo = StudentRepository()
            repo.delete(student.id)
            self._load_students()
    
    def _on_payment(self):
        """Gère le clic sur le bouton Enregistrer paiement."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        student_data = self.current_students[row]
        student = student_data['student']
        
        from src.ui.payment_dialog import PaymentDialog
        dialog = PaymentDialog(self, student.id)
        if dialog.exec():
            self._load_students()
    
    def _on_search(self, text: str):
        """Gère la recherche par nom/prénom."""
        if not text:
            self._load_students()
            return
        
        from src.repositories.student_repository import StudentRepository
        repo = StudentRepository()
        students = repo.search_by_name(text)
        
        # Ajouter les infos de statut
        self.current_students = []
        for student in students:
            balance = self.student_service.calculate_balance(student.id)
            status = self.student_service.get_payment_status(student.id)
            total_paid = self.student_service.payment_repo.get_sum_by_student(student.id)
            
            self.current_students.append({
                'student': student,
                'total_paid': total_paid,
                'balance': balance,
                'status': status
            })
        
        self._update_table()
    
    def _on_filter_changed(self, classe: str):
        """Gère le changement de filtre par classe."""
        if classe == "Toutes les classes":
            self._load_students()
            return
        
        from src.repositories.student_repository import StudentRepository
        repo = StudentRepository()
        students = repo.filter_by_class(classe)
        
        # Ajouter les infos de statut
        self.current_students = []
        for student in students:
            balance = self.student_service.calculate_balance(student.id)
            status = self.student_service.get_payment_status(student.id)
            total_paid = self.student_service.payment_repo.get_sum_by_student(student.id)
            
            self.current_students.append({
                'student': student,
                'total_paid': total_paid,
                'balance': balance,
                'status': status
            })
        
        self._update_table()
    
    def _on_double_click(self, index):
        """Gère le double-clic sur une ligne."""
        row = index.row()
        student_data = self.current_students[row]
        
        from src.ui.student_detail import StudentDetailDialog
        dialog = StudentDetailDialog(student_data['student'].id, self)
        dialog.exec()
        self.refresh()
    
    def _show_context_menu(self, position):
        """Affiche le menu contextuel."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        menu = QMenu(self)
        
        action_view = QAction("Voir les détails", self)
        action_view.triggered.connect(self._on_view_details)
        menu.addAction(action_view)
        
        action_payment = QAction("Enregistrer un paiement", self)
        action_payment.triggered.connect(self._on_payment)
        menu.addAction(action_payment)
        
        menu.addSeparator()
        
        action_edit = QAction("Modifier", self)
        action_edit.triggered.connect(self._on_edit)
        menu.addAction(action_edit)
        
        action_delete = QAction("Supprimer", self)
        action_delete.triggered.connect(self._on_delete)
        menu.addAction(action_delete)
        
        menu.exec(self.table.viewport().mapToGlobal(position))
    
    def _on_view_details(self):
        """Gère l'action de voir les détails."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        student_data = self.current_students[row]
        
        from src.ui.student_detail import StudentDetailDialog
        dialog = StudentDetailDialog(student_data['student'].id, self)
        dialog.exec()
        self.refresh()
    
    def refresh(self):
        """Actualise la liste des élèves."""
        self._load_students()
