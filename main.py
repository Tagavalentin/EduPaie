import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.error_handler import setup_error_handler


def main():
    # Configurer le gestionnaire d'erreurs
    setup_error_handler()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
