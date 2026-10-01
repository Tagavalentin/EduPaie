import sqlite3
from pathlib import Path
import re
import argparse
from .connection import get_connection
from src.utils.paths import get_base_path


def _migrate_payment_modes(conn: sqlite3.Connection) -> None:
    """Restore the four-mode constraint without rewriting historical custom modes."""
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'payments'"
    ).fetchone()
    if not row:
        return

    normalized_schema = re.sub(r"\s+", "", row[0]).lower()
    if "check(length(trim(mode_paiement))>0)" not in normalized_schema:
        return

    custom_mode_exists = conn.execute(
        """SELECT 1 FROM payments
           WHERE mode_paiement NOT IN ('especes', 'cheque', 'virement', 'mobile_money')
           LIMIT 1"""
    ).fetchone()
    if custom_mode_exists:
        return

    conn.execute("""
        CREATE TABLE payments_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            montant INTEGER NOT NULL CHECK (montant > 0),
            date_paiement TEXT NOT NULL,
            mode_paiement TEXT NOT NULL CHECK (
                mode_paiement IN ('especes', 'cheque', 'virement', 'mobile_money')
            ),
            numero_recu TEXT UNIQUE NOT NULL,
            solde_apres INTEGER NOT NULL CHECK (solde_apres >= 0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE RESTRICT
        )
    """)
    conn.execute("""
        INSERT INTO payments_new
        SELECT id, student_id, montant, date_paiement, mode_paiement,
               numero_recu, solde_apres, created_at
        FROM payments
    """)
    conn.execute("DROP TABLE payments")
    conn.execute("ALTER TABLE payments_new RENAME TO payments")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_payments_student_id ON payments(student_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_payments_numero_recu ON payments(numero_recu)")


def init_database(include_demo_data: bool = False) -> None:
    """
    Initialise le schéma et ajoute les données de démonstration sur demande.
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

        _migrate_payment_modes(conn)

        # Ne charger les données de démonstration que sur demande.
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        
        if student_count == 0 and include_demo_data:
            if seed_path.exists():
                with open(seed_path, 'r', encoding='utf-8') as f:
                    seed_sql = f.read()
                    cursor.executescript(seed_sql)
                print("Données de démonstration insérées avec succès.")
            else:
                print(f"Fichier de démonstration introuvable : {seed_path}")
        elif student_count > 0:
            print(f"La base contient déjà {student_count} élève(s). Aucune donnée de démonstration ajoutée.")
        else:
            print("Base de données créée sans données de démonstration.")
        
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
    parser = argparse.ArgumentParser(description="Initialiser la base de données EduPaie.")
    parser.add_argument(
        "--demo-data",
        action="store_true",
        help="Insérer les données de démonstration si la base est vide.",
    )
    args = parser.parse_args()
    init_database(include_demo_data=args.demo_data)
