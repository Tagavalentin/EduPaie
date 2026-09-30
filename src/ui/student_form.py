from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QLineEdit, QSpinBox, QPushButton, QMessageBox)
from PySide6.QtCore import Qt

from src.models.student import Student
from src.repositories.student_repository import StudentRepository


class StudentForm(QDialog):
    """Formulaire d'ajout/modification d'un élève."""
    
    def __init__(self, parent=None, student: Student = None):
        super().__init__(parent)
        self.student = student
        self.repo = StudentRepository()
        
        self.setWindowTitle("Ajouter un élève" if student is None else "Modifier un élève")
        self.setMinimumWidth(400)
        
        self._setup_ui()
        
        if student:
            self._fill_form()
    
    def _setup_ui(self):
        """Configure l'interface du formulaire."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Nom
        nom_layout = QHBoxLayout()
        nom_label = QLabel("Nom *:")
        nom_label.setFixedWidth(100)
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom de l'élève")
        nom_layout.addWidget(nom_label)
        nom_layout.addWidget(self.nom_input)
        layout.addLayout(nom_layout)
        
        # Prénom
        prenom_layout = QHBoxLayout()
        prenom_label = QLabel("Prénom *:")
        prenom_label.setFixedWidth(100)
        self.prenom_input = QLineEdit()
        self.prenom_input.setPlaceholderText("Prénom de l'élève")
        prenom_layout.addWidget(prenom_label)
        prenom_layout.addWidget(self.prenom_input)
        layout.addLayout(prenom_layout)
        
        # Classe
        classe_layout = QHBoxLayout()
        classe_label = QLabel("Classe *:")
        classe_label.setFixedWidth(100)
        self.classe_input = QLineEdit()
        self.classe_input.setPlaceholderText("Ex: 6ème A")
        classe_layout.addWidget(classe_label)
        classe_layout.addWidget(self.classe_input)
        layout.addLayout(classe_layout)
        
        # Année scolaire
        annee_layout = QHBoxLayout()
        annee_label = QLabel("Année *:")
        annee_label.setFixedWidth(100)
        self.annee_input = QLineEdit()
        self.annee_input.setPlaceholderText("Ex: 2025-2026")
        self.annee_input.setText("2025-2026")
        annee_layout.addWidget(annee_label)
        annee_layout.addWidget(self.annee_input)
        layout.addLayout(annee_layout)
        
        # Total dû
        total_layout = QHBoxLayout()
        total_label = QLabel("Total dû (FCFA) *:")
        total_label.setFixedWidth(100)
        self.total_input = QSpinBox()
        self.total_input.setRange(0, 999999999)
        self.total_input.setSingleStep(5000)
        self.total_input.setSuffix(" FCFA")
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_input)
        layout.addLayout(total_layout)
        
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
    
    def _fill_form(self):
        """Remplit le formulaire avec les données de l'élève."""
        self.nom_input.setText(self.student.nom)
        self.prenom_input.setText(self.student.prenom)
        self.classe_input.setText(self.student.classe)
        self.annee_input.setText(self.student.annee_scolaire)
        self.total_input.setValue(self.student.total_du)
    
    def _validate(self):
        """Valide les champs du formulaire."""
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        classe = self.classe_input.text().strip()
        annee = self.annee_input.text().strip()
        total = self.total_input.value()
        
        if not nom:
            return False, "Le nom est obligatoire."
        
        if not prenom:
            return False, "Le prénom est obligatoire."
        
        if not classe:
            return False, "La classe est obligatoire."
        
        if not annee:
            return False, "L'année scolaire est obligatoire."
        
        if total < 0:
            return False, "Le total dû doit être positif ou nul."
        
        return True, ""
    
    def _on_save(self):
        """Gère l'enregistrement."""
        is_valid, error_msg = self._validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Erreur de validation", error_msg)
            return
        
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        classe = self.classe_input.text().strip()
        annee = self.annee_input.text().strip()
        total = self.total_input.value()
        
        try:
            if self.student:
                # Modification
                self.student.nom = nom
                self.student.prenom = prenom
                self.student.classe = classe
                self.student.annee_scolaire = annee
                self.student.total_du = total
                self.repo.update(self.student)
            else:
                # Création
                student = Student(
                    id=None,
                    nom=nom,
                    prenom=prenom,
                    classe=classe,
                    annee_scolaire=annee,
                    total_du=total
                )
                self.repo.create(student)
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement : {str(e)}")
