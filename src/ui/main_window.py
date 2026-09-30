from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduPaie - Gestion des paiements scolaires")
        self.setMinimumSize(1024, 768)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Placeholder widget
        placeholder = QWidget()
        self.stack.addWidget(placeholder)
