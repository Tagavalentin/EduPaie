import sys
import logging
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import QMessageBox

from src.utils.paths import get_log_file_path


def setup_error_handler():
    """Configure le gestionnaire d'erreurs global."""
    # Configurer le logging
    log_file = get_log_file_path()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Démarrage de l'application EduPaie")
    
    # Remplacer le hook d'exception par défaut
    sys.excepthook = exception_hook


def exception_hook(exc_type, exc_value, exc_traceback):
    """
    Hook global pour capturer les exceptions non gérées.
    Affiche une QMessageBox et log l'erreur.
    """
    logger = logging.getLogger(__name__)
    
    # Logger l'erreur
    error_msg = "".join([
        f"Type: {exc_type.__name__}\n",
        f"Value: {exc_value}\n",
        f"Traceback: {''.join(logging.traceback.format_tb(exc_traceback))}"
    ])
    logger.error(f"Exception non gérée:\n{error_msg}")
    
    # Afficher une QMessageBox si QApplication est disponible
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        
        if app:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Erreur")
            msg.setText("Une erreur inattendue s'est produite.")
            msg.setDetailedText(str(exc_value))
            msg.exec()
    except:
        # Si QApplication n'est pas disponible ou plante
        pass
    
    # Appeler le hook par défaut
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


def log_info(message: str):
    """Log un message d'information."""
    logger = logging.getLogger(__name__)
    logger.info(message)


def log_warning(message: str):
    """Log un avertissement."""
    logger = logging.getLogger(__name__)
    logger.warning(message)


def log_error(message: str):
    """Log une erreur."""
    logger = logging.getLogger(__name__)
    logger.error(message)
