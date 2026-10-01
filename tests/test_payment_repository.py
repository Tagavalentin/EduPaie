import sqlite3
import pytest
from datetime import datetime

from src.repositories.payment_repository import PaymentRepository
from src.models.payment import Payment


@pytest.fixture
def in_memory_db():
    """Fixture pour une base de données SQLite en mémoire."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    
    # Créer le schéma
    conn.executescript("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            classe TEXT NOT NULL,
            annee_scolaire TEXT NOT NULL,
            total_du INTEGER NOT NULL CHECK (total_du >= 0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            montant INTEGER NOT NULL CHECK (montant > 0),
            date_paiement TEXT NOT NULL,
            mode_paiement TEXT NOT NULL CHECK (mode_paiement IN ('especes', 'cheque', 'virement', 'mobile_money')),
            numero_recu TEXT UNIQUE NOT NULL,
            solde_apres INTEGER NOT NULL CHECK (solde_apres >= 0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE RESTRICT
        );
    """)
    
    yield conn
    conn.close()


@pytest.fixture
def repo(in_memory_db, monkeypatch):
    """Fixture pour le repository avec la base en mémoire."""
    import src.repositories.payment_repository as repo_module
    monkeypatch.setattr(repo_module, 'get_connection', lambda: in_memory_db)
    monkeypatch.setattr(repo_module, 'close_connection', lambda conn: None)
    
    return PaymentRepository()


@pytest.fixture
def student_id(in_memory_db):
    """Fixture pour créer un élève de test."""
    cursor = in_memory_db.cursor()
    cursor.execute(
        "INSERT INTO students (nom, prenom, classe, annee_scolaire, total_du) VALUES (?, ?, ?, ?, ?)",
        ("Test", "Eleve", "6ème A", "2025-2026", 150000)
    )
    in_memory_db.commit()
    return cursor.lastrowid


def test_create_payment(repo, student_id):
    """Test la création d'un paiement."""
    payment = Payment(
        id=None,
        student_id=student_id,
        montant=50000,
        date_paiement="2025-09-15",
        mode_paiement="especes",
        numero_recu="REC-2025-000001",
        solde_apres=100000
    )
    
    created = repo.create(payment)
    
    assert created.id is not None
    assert created.student_id == student_id
    assert created.montant == 50000
    assert created.mode_paiement == "especes"
    assert created.numero_recu == "REC-2025-000001"
    assert created.solde_apres == 100000


def test_get_by_id(repo, student_id):
    """Test la récupération d'un paiement par id."""
    payment = Payment(
        id=None,
        student_id=student_id,
        montant=75000,
        date_paiement="2025-10-20",
        mode_paiement="virement",
        numero_recu="REC-2025-000002",
        solde_apres=75000
    )
    created = repo.create(payment)
    
    found = repo.get_by_id(created.id)
    
    assert found is not None
    assert found.id == created.id
    assert found.montant == 75000
    assert found.numero_recu == "REC-2025-000002"


def test_get_by_id_not_found(repo):
    """Test la récupération d'un paiement inexistant."""
    found = repo.get_by_id(999)
    assert found is None


def test_get_by_receipt_number(repo, student_id):
    """Test la récupération d'un paiement par numéro de reçu."""
    payment = Payment(
        id=None,
        student_id=student_id,
        montant=25000,
        date_paiement="2025-09-10",
        mode_paiement="mobile_money",
        numero_recu="REC-2025-000003",
        solde_apres=125000
    )
    repo.create(payment)
    
    found = repo.get_by_receipt_number("REC-2025-000003")
    
    assert found is not None
    assert found.numero_recu == "REC-2025-000003"
    assert found.montant == 25000


def test_get_by_receipt_number_not_found(repo):
    """Test la récupération par numéro de reçu inexistant."""
    found = repo.get_by_receipt_number("REC-999")
    assert found is None


def test_get_by_student(repo, student_id):
    """Test la récupération des paiements d'un élève."""
    repo.create(Payment(None, student_id, 50000, "2025-09-15", "especes", "REC-001", 100000))
    repo.create(Payment(None, student_id, 25000, "2025-10-20", "mobile_money", "REC-002", 75000))
    repo.create(Payment(None, student_id, 75000, "2025-11-10", "virement", "REC-003", 0))
    
    payments = repo.get_by_student(student_id)
    
    assert len(payments) == 3
    assert all(p.student_id == student_id for p in payments)
    # Vérifier l'ordre chronologique décroissant
    assert payments[0].date_paiement >= payments[1].date_paiement
    assert payments[1].date_paiement >= payments[2].date_paiement


def test_get_all(repo, in_memory_db):
    """Test la récupération de tous les paiements."""
    # Créer deux élèves
    cursor = in_memory_db.cursor()
    cursor.execute(
        "INSERT INTO students (nom, prenom, classe, annee_scolaire, total_du) VALUES (?, ?, ?, ?, ?)",
        ("Test1", "Eleve1", "6ème A", "2025-2026", 150000)
    )
    student1_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO students (nom, prenom, classe, annee_scolaire, total_du) VALUES (?, ?, ?, ?, ?)",
        ("Test2", "Eleve2", "6ème B", "2025-2026", 150000)
    )
    student2_id = cursor.lastrowid
    in_memory_db.commit()
    
    repo.create(Payment(None, student1_id, 50000, "2025-09-15", "especes", "REC-001", 100000))
    repo.create(Payment(None, student2_id, 75000, "2025-10-20", "virement", "REC-002", 75000))
    
    payments = repo.get_all()
    
    assert len(payments) == 2


def test_get_sum_by_student(repo, student_id):
    """Test le calcul de la somme des paiements d'un élève."""
    repo.create(Payment(None, student_id, 50000, "2025-09-15", "especes", "REC-001", 100000))
    repo.create(Payment(None, student_id, 25000, "2025-10-20", "mobile_money", "REC-002", 75000))
    repo.create(Payment(None, student_id, 75000, "2025-11-10", "virement", "REC-003", 0))
    
    total = repo.get_sum_by_student(student_id)
    
    assert total == 150000


def test_get_sum_by_student_no_payments(repo, student_id):
    """Test le calcul de la somme pour un élève sans paiements."""
    total = repo.get_sum_by_student(student_id)
    assert total == 0


def test_delete_payment(repo, student_id):
    """Test la suppression d'un paiement."""
    payment = repo.create(Payment(None, student_id, 50000, "2025-09-15", "especes", "REC-001", 100000))
    
    result = repo.delete(payment.id)
    
    assert result is True
    assert repo.get_by_id(payment.id) is None


def test_delete_payment_not_found(repo):
    """Test la suppression d'un paiement inexistant."""
    result = repo.delete(999)
    assert result is False
