from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                 QPushButton, QStackedWidget, QLabel, QFrame)
from PySide6.QtCore import Qt

from src.ui.students_view import StudentsView


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application EduPaie."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduPaie - Gestion des paiements scolaires")
        self.setMinimumSize(1024, 768)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Barre latérale
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Zone de contenu
        self.content_area = QWidget()
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        self.header = self._create_header()
        content_layout.addWidget(self.header)
        
        # Stack pour les vues
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
        main_layout.addWidget(self.content_area, stretch=1)
        
        # Créer les vues
        self._create_views()
        
        # Appliquer le style
        self._apply_style()
    
    def _create_sidebar(self) -> QWidget:
        """Crée la barre latérale avec les boutons de navigation."""
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)
        
        # Logo/Titre
        title = QLabel("EduPaie")
        title.setObjectName("sidebarTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Bouton Tableau de bord
        self.btn_dashboard = QPushButton("Tableau de bord")
        self.btn_dashboard.setObjectName("sidebarButton")
        self.btn_dashboard.clicked.connect(lambda: self._show_view("dashboard"))
        layout.addWidget(self.btn_dashboard)
        
        # Bouton Élèves
        self.btn_students = QPushButton("Élèves")
        self.btn_students.setObjectName("sidebarButton")
        self.btn_students.clicked.connect(lambda: self._show_view("students"))
        layout.addWidget(self.btn_students)
        
        layout.addStretch()
        
        # Bouton Quitter
        self.btn_quit = QPushButton("Quitter")
        self.btn_quit.setObjectName("sidebarButtonQuit")
        self.btn_quit.clicked.connect(self.close)
        layout.addWidget(self.btn_quit)
        
        return sidebar
    
    def _create_header(self) -> QWidget:
        """Crée l'en-tête de la zone de contenu."""
        header = QWidget()
        header.setFixedHeight(60)
        header.setObjectName("header")
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        self.header_title = QLabel("Tableau de bord")
        self.header_title.setObjectName("headerTitle")
        layout.addWidget(self.header_title)
        
        layout.addStretch()
        
        return header
    
    def _create_views(self):
        """Crée les différentes vues de l'application."""
        # Vue Tableau de bord (placeholder)
        self.dashboard_view = QWidget()
        dashboard_layout = QVBoxLayout(self.dashboard_view)
        dashboard_label = QLabel("Tableau de bord - En construction")
        dashboard_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dashboard_layout.addWidget(dashboard_label)
        self.stack.addWidget(self.dashboard_view)
        
        # Vue Élèves
        self.students_view = StudentsView()
        self.students_view.student_selected.connect(self._on_student_selected)
        self.stack.addWidget(self.students_view)
    
    def _show_view(self, view_name: str):
        """Affiche la vue demandée."""
        if view_name == "dashboard":
            self.stack.setCurrentWidget(self.dashboard_view)
            self.header_title.setText("Tableau de bord")
            self._update_active_button(self.btn_dashboard)
        elif view_name == "students":
            self.stack.setCurrentWidget(self.students_view)
            self.header_title.setText("Gestion des élèves")
            self._update_active_button(self.btn_students)
    
    def _update_active_button(self, active_button: QPushButton):
        """Met à jour l'apparence des boutons de la barre latérale."""
        buttons = [self.btn_dashboard, self.btn_students]
        for btn in buttons:
            if btn == active_button:
                btn.setProperty("active", True)
            else:
                btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
    
    def _on_student_selected(self, student_id: int):
        """Gère la sélection d'un élève."""
        # Pour l'instant, juste un placeholder
        # La fiche élève sera implémentée dans la branche feature/fiche-eleve-historique
        print(f"Élève sélectionné : {student_id}")
    
    def _apply_style(self):
        """Applique la feuille de style commune."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            #sidebar {
                background-color: #2c3e50;
                color: white;
            }
            
            #sidebarTitle {
                font-size: 24px;
                font-weight: bold;
                color: white;
                padding: 10px;
            }
            
            #sidebarButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 5px;
                font-size: 14px;
            }
            
            #sidebarButton:hover {
                background-color: #3d566e;
            }
            
            #sidebarButton[active="true"] {
                background-color: #3498db;
            }
            
            #sidebarButtonQuit {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 5px;
                font-size: 14px;
            }
            
            #sidebarButtonQuit:hover {
                background-color: #c0392b;
            }
            
            #header {
                background-color: white;
                border-bottom: 1px solid #ddd;
            }
            
            #headerTitle {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
            }
            
            QStackedWidget {
                background-color: white;
            }
        """)
