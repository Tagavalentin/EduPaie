import sqlite3
from pathlib import Path
from typing import Optional

from src.utils.paths import get_db_path


def get_connection() -> sqlite3.Connection:
    """
    Crée et retourne une connexion à la base de données.
    Active les clés étrangères.
    """
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def close_connection(conn: Optional[sqlite3.Connection]) -> None:
    """Ferme la connexion si elle est ouverte."""
    if conn:
        conn.close()
