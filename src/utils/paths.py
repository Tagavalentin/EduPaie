import sys
import os
from pathlib import Path
from datetime import datetime


def get_base_path() -> Path:
    """
    Retourne le chemin de base de l'application.
    Gère le cas où l'application est packagée avec PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        # Application packagée
        return Path(sys._MEIPASS)
    else:
        # En développement
        return Path(__file__).parent.parent.parent


def get_data_path() -> Path:
    """
    Retourne le chemin vers le dossier des données.
    Pour les applications packagées, utilise un dossier utilisateur.
    """
    if getattr(sys, 'frozen', False):
        # Application packagée : utiliser un dossier utilisateur
        if os.name == 'nt':  # Windows
            local_app_data = os.environ.get("LOCALAPPDATA")
            base_path = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
            data_path = base_path / "EduPaie"
        else:  # macOS/Linux
            data_path = Path.home() / ".edupaie"
    else:
        # En développement : utiliser le dossier data du projet
        data_path = get_base_path() / "data"
    
    data_path.mkdir(parents=True, exist_ok=True)
    return data_path


def get_log_file_path() -> Path:
    """
    Retourne le chemin vers le fichier de log.
    """
    log_dir = Path.home() / ".edupaie" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    return log_dir / f"edupaie_{datetime.now().strftime('%Y%m%d')}.log"


def get_db_path() -> Path:
    """
    Retourne le chemin vers la base de données.
    """
    return get_data_path() / "edupaie.db"
