import sqlite3
from pathlib import Path
from .connection import get_connection
from src.utils.paths import get_base_path


def init_database() -> None:
    """
    Initialise la base de données avec le schéma et les données de test.
    Crée les tables si elles n'existent pas.
    """
    base_path = get_base_path()
    schema_path = base_path / "sql" / "schema.sql"
    seed_path = base_path / "sql" / "seed.sql"
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Exécuter le schéma
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
                cursor.executescript(schema_sql)
            print("Schéma de la base de données créé avec succès.")
        else:
            print(f"Fichier schéma introuvable : {schema_path}")
        
        # Exécuter les données de test (seulement si la base est vide)
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        
        if student_count == 0 and seed_path.exists():
            with open(seed_path, 'r', encoding='utf-8') as f:
                seed_sql = f.read()
                cursor.executescript(seed_sql)
            print("Données de test insérées avec succès.")
        elif student_count > 0:
            print(f"La base contient déjà {student_count} élève(s). Pas d'insertion de données de test.")
        else:
            print(f"Fichier seed introuvable : {seed_path}")
        
        conn.commit()
        from src.utils.paths import get_db_path
        print(f"Base de données initialisée : {get_db_path()}")
        
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'initialisation de la base : {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
