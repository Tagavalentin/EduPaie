from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QPushButton, QTableView, QHeaderView, QComboBox,
                                 QGroupBox, QGridLayout)
from PySide6.QtCore import Qt

from src.services.dashboard_service import DashboardService
from src.services.student_service import PaymentStatus
from src.utils.formatters import format_fcfa


class DashboardView(QWidget):
    """Vue du tableau de bord avec statistiques."""
    
    def __init__(self):
        super().__init__()
        self.dashboard_service = DashboardService()
        self.card_students_value = None
        self.card_paid_value = None
        self.card_remaining_value = None
        self.card_unpaid_value = None
        
        self._setup_ui()
        self._load_statistics()
    
    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Cartes de statistiques
        stats_layout = QGridLayout()
        stats_layout.setHorizontalSpacing(16)
        stats_layout.setVerticalSpacing(16)
        
        # Carte 1: Nombre d'élèves
        self.card_students, self.card_students_value = self._create_stat_card("Nombre d'élèves", "0", "#3498db")
        stats_layout.addWidget(self.card_students, 0, 0)
        
        # Carte 2: Total encaissé
        self.card_paid, self.card_paid_value = self._create_stat_card("Total encaissé", "0 FCFA", "#27ae60")
        stats_layout.addWidget(self.card_paid, 0, 1)
        
        # Carte 3: Total restant
        self.card_remaining, self.card_remaining_value = self._create_stat_card("Total restant dû", "0 FCFA", "#e74c3c")
        stats_layout.addWidget(self.card_remaining, 0, 2)
        
        # Carte 4: Élèves non soldés
        self.card_unpaid, self.card_unpaid_value = self._create_stat_card("Élèves non soldés", "0", "#e67e22")
        stats_layout.addWidget(self.card_unpaid, 0, 3)
        
        layout.addLayout(stats_layout)
        
        # Liste des élèves par statut
        list_group = QGroupBox("Liste des élèves")
        list_layout = QVBoxLayout(list_group)
        
        # Filtre par statut
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filtrer par statut :")
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Tous", "Soldé", "Partiellement payé", "Non payé"])
        self.status_filter.currentTextChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addStretch()
        
        self.btn_refresh = QPushButton("Actualiser")
        self.btn_refresh.clicked.connect(self._load_statistics)
        filter_layout.addWidget(self.btn_refresh)
        
        list_layout.addLayout(filter_layout)
        
        # Tableau
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical_header = self.table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical_header.setMinimumSectionSize(40)
        
        list_layout.addWidget(self.table)
        
        layout.addWidget(list_group)
    
    def _create_stat_card(self, title: str, value: str, color: str):
        """Crée une carte de statistique."""
        card = QGroupBox()
        card.setStyleSheet(f"""
            QGroupBox {{
                border: 2px solid {color};
                border-radius: 8px;
                margin-top: 10px;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: {color};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 24, 16, 16)
        
        card_title = QLabel(title)
        card_title.setStyleSheet(f"color: {color}; font-size: 14px;")
        layout.addWidget(card_title)
        
        card_value = QLabel(value)
        card_value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        layout.addWidget(card_value)
        
        return card, card_value
    
    def _load_statistics(self):
        """Charge et affiche les statistiques."""
        stats = self.dashboard_service.get_statistics()
        
        # Mettre à jour les cartes
        self.card_students_value.setText(str(stats['total_students']))
        self.card_paid_value.setText(format_fcfa(stats['total_paid']))
        self.card_remaining_value.setText(format_fcfa(stats['total_remaining']))
        self.card_unpaid_value.setText(str(stats['unpaid_students_count']))
        
        # Charger la liste des élèves
        self._load_students_list()
    
    def _load_students_list(self, status_filter: str = "Tous"):
        """Charge la liste des élèves selon le filtre."""
        if status_filter == "Tous":
            students_data = self.dashboard_service.student_service.get_all_students_with_status()
        elif status_filter == "Soldé":
            students_data = self.dashboard_service.get_students_by_status(PaymentStatus.PAID)
        elif status_filter == "Partiellement payé":
            students_data = self.dashboard_service.get_students_by_status(PaymentStatus.PARTIAL)
        elif status_filter == "Non payé":
            students_data = self.dashboard_service.get_students_by_status(PaymentStatus.UNPAID)
        else:
            students_data = []
        
        from src.ui.students_table_model import StudentsTableModel
        model = StudentsTableModel(students_data)
        self.table.setModel(model)
    
    def _on_filter_changed(self, text: str):
        """Gère le changement de filtre."""
        self._load_students_list(text)
    
    def refresh(self):
        """Actualise les statistiques."""
        self._load_statistics()
