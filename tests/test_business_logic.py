import sqlite3
import pytest
from datetime import datetime

from src.services.student_service import StudentService, PaymentStatus
from src.services.payment_service import PaymentService
from src.repositories.student_repository import StudentRepository
from src.repositories.payment_repository import PaymentRepository
from src.models.student import Student
from src.models.payment import Payment
from src.database.init_db import _migrate_payment_modes


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
def student_id(in_memory_db):
    """Fixture pour créer un élève de test avec total_du = 150000."""
    cursor = in_memory_db.cursor()
    cursor.execute(
        "INSERT INTO students (nom, prenom, classe, annee_scolaire, total_du) VALUES (?, ?, ?, ?, ?)",
        ("Test", "Eleve", "6ème A", "2025-2026", 150000)
    )
    in_memory_db.commit()
    return cursor.lastrowid


@pytest.fixture
def services(in_memory_db, monkeypatch):
    """Fixture pour les services avec la base en mémoire."""
    import src.services.student_service as student_service_module
    import src.services.payment_service as payment_service_module
    import src.repositories.student_repository as student_repo_module
    import src.repositories.payment_repository as payment_repo_module
    import src.database.connection as connection_module
    
    monkeypatch.setattr(student_repo_module, 'get_connection', lambda: in_memory_db)
    monkeypatch.setattr(student_repo_module, 'close_connection', lambda conn: None)
    monkeypatch.setattr(payment_repo_module, 'get_connection', lambda: in_memory_db)
    monkeypatch.setattr(payment_repo_module, 'close_connection', lambda conn: None)
    monkeypatch.setattr(payment_service_module, 'get_connection', lambda: in_memory_db)
    monkeypatch.setattr(payment_service_module, 'close_connection', lambda conn: None)
    monkeypatch.setattr(connection_module, 'get_connection', lambda: in_memory_db)
    monkeypatch.setattr(connection_module, 'close_connection', lambda conn: None)
    
    return StudentService(), PaymentService()


# Tests StudentService
def test_calculate_balance_no_payments(services, student_id):
    """Test le calcul du solde pour un élève sans paiements."""
    student_service, _ = services
    balance = student_service.calculate_balance(student_id)
    assert balance == 150000


def test_calculate_balance_partial_payments(services, student_id, in_memory_db):
    """Test le calcul du solde pour un élève avec paiements partiels."""
    student_service, _ = services
    
    # Ajouter des paiements
    in_memory_db.execute(
        "INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, 50000, "2025-09-15", "especes", "REC-001", 100000)
    )
    in_memory_db.execute(
        "INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, 25000, "2025-10-20", "mobile_money", "REC-002", 75000)
    )
    in_memory_db.commit()
    
    balance = student_service.calculate_balance(student_id)
    assert balance == 75000


def test_calculate_balance_fully_paid(services, student_id, in_memory_db):
    """Test le calcul du solde pour un élève soldé."""
    student_service, _ = services
    
    # Ajouter des paiements pour solder
    in_memory_db.execute(
        "INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, 150000, "2025-09-15", "especes", "REC-001", 0)
    )
    in_memory_db.commit()
    
    balance = student_service.calculate_balance(student_id)
    assert balance == 0


def test_get_payment_status_unpaid(services, student_id):
    """Test le statut pour un élève non payé."""
    student_service, _ = services
    status = student_service.get_payment_status(student_id)
    assert status == PaymentStatus.PARTIAL  # Solde > 0


def test_get_payment_status_partial(services, student_id, in_memory_db):
    """Test le statut pour un élève partiellement payé."""
    student_service, _ = services
    
    in_memory_db.execute(
        "INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, 50000, "2025-09-15", "especes", "REC-001", 100000)
    )
    in_memory_db.commit()
    
    status = student_service.get_payment_status(student_id)
    assert status == PaymentStatus.PARTIAL


def test_get_payment_status_paid(services, student_id, in_memory_db):
    """Test le statut pour un élève soldé."""
    student_service, _ = services
    
    in_memory_db.execute(
        "INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, 150000, "2025-09-15", "especes", "REC-001", 0)
    )
    in_memory_db.commit()
    
    status = student_service.get_payment_status(student_id)
    assert status == PaymentStatus.PAID


def test_can_delete_student_no_payments(services, student_id):
    """Test la suppression d'un élève sans paiements."""
    student_service, _ = services
    can_delete, msg = student_service.can_delete_student(student_id)
    assert can_delete is True
    assert msg == ""


def test_can_delete_student_with_payments(services, student_id, in_memory_db):
    """Test la suppression d'un élève avec paiements."""
    student_service, _ = services
    
    in_memory_db.execute(
        "INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, 50000, "2025-09-15", "especes", "REC-001", 100000)
    )
    in_memory_db.commit()
    
    can_delete, msg = student_service.can_delete_student(student_id)
    assert can_delete is False
    assert "paiements" in msg.lower()


# Tests PaymentService
def test_validate_payment_amount_positive(services, student_id):
    """Test la validation d'un montant positif."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_amount(50000, student_id)
    assert is_valid is True
    assert msg == ""


def test_validate_payment_amount_zero(services, student_id):
    """Test la validation d'un montant nul."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_amount(0, student_id)
    assert is_valid is False
    assert "positif" in msg.lower()


def test_validate_payment_amount_negative(services, student_id):
    """Test la validation d'un montant négatif."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_amount(-500, student_id)
    assert is_valid is False
    assert "positif" in msg.lower()


def test_validate_payment_amount_decimal(services, student_id):
    """Test la validation d'un montant décimal."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_amount(1500.5, student_id)
    assert is_valid is False
    assert "entier" in msg.lower()


def test_validate_payment_amount_text(services, student_id):
    """Test la validation d'un montant texte."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_amount("abc", student_id)
    assert is_valid is False
    assert "entier" in msg.lower()


def test_validate_payment_amount_exceeds_balance(services, student_id):
    """Test la validation d'un montant supérieur au solde."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_amount(200000, student_id)
    assert is_valid is False
    assert "dépasse" in msg.lower()


def test_validate_payment_amount_equals_balance(services, student_id):
    """Test la validation d'un montant égal au solde."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_amount(150000, student_id)
    assert is_valid is True
    assert msg == ""


def test_validate_payment_date_valid(services):
    """Test la validation d'une date valide."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_date("2025-09-15")
    assert is_valid is True
    assert msg == ""


def test_validate_payment_date_invalid(services):
    """Test la validation d'une date invalide."""
    _, payment_service = services
    is_valid, msg = payment_service.validate_payment_date("15/09/2025")
    assert is_valid is False
    assert "format" in msg.lower()


def test_generate_receipt_number(services):
    """Test la génération d'un numéro de reçu (format)."""
    _, payment_service = services
    
    # Générer un numéro
    receipt = payment_service.generate_receipt_number(2025)
    
    # Vérifier le format
    assert receipt.startswith("REC-2025-")
    parts = receipt.split("-")
    assert len(parts) == 3
    assert parts[0] == "REC"
    assert parts[1] == "2025"
    assert parts[2].isdigit()
    assert len(parts[2]) == 6  # Padding à 6 chiffres


def test_create_payment_success(services, student_id):
    """Test la création d'un paiement valide."""
    _, payment_service = services
    
    payment, error = payment_service.create_payment(
        student_id=student_id,
        amount=50000,
        date_paiement="2025-09-15",
        mode_paiement="especes"
    )
    
    assert payment is not None
    assert error == ""
    assert payment.montant == 50000
    assert payment.solde_apres == 100000
    assert payment.numero_recu.startswith("REC-2025-")


def test_create_payment_invalid_amount(services, student_id):
    """Test la création d'un paiement avec montant invalide."""
    _, payment_service = services
    
    payment, error = payment_service.create_payment(
        student_id=student_id,
        amount=200000,
        date_paiement="2025-09-15",
        mode_paiement="especes"
    )
    
    assert payment is None
    assert "dépasse" in error.lower()


def test_create_payment_invalid_date(services, student_id):
    """Test la création d'un paiement avec date invalide."""
    _, payment_service = services
    
    payment, error = payment_service.create_payment(
        student_id=student_id,
        amount=50000,
        date_paiement="15/09/2025",
        mode_paiement="especes"
    )
    
    assert payment is None
    assert "format" in error.lower()


def test_create_payment_invalid_mode(services, student_id):
    """Test le refus d'un mode qui n'est pas dans la liste autorisée."""
    _, payment_service = services
    
    payment, error = payment_service.create_payment(
        student_id=student_id,
        amount=50000,
        date_paiement="2025-09-15",
        mode_paiement="carte_bancaire"
    )
    
    assert payment is None
    assert "mode invalide" in error.lower()


@pytest.mark.parametrize("mode", ["especes", "cheque", "virement", "mobile_money"])
def test_create_payment_allowed_modes(services, student_id, mode):
    _, payment_service = services

    payment, error = payment_service.create_payment(
        student_id=student_id,
        amount=50000,
        date_paiement="2025-09-15",
        mode_paiement=mode
    )

    assert payment is not None
    assert payment.mode_paiement == mode
    assert error == ""


def test_migrate_loose_payment_modes_preserves_existing_payments():
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            classe TEXT NOT NULL,
            annee_scolaire TEXT NOT NULL,
            total_du INTEGER NOT NULL
        );
        INSERT INTO students VALUES (1, 'Test', 'Eleve', '6ème A', '2025-2026', 100000);
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            montant INTEGER NOT NULL,
            date_paiement TEXT NOT NULL,
            mode_paiement TEXT NOT NULL CHECK (length(trim(mode_paiement)) > 0),
            numero_recu TEXT UNIQUE NOT NULL,
            solde_apres INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
        INSERT INTO payments (id, student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres)
        VALUES (1, 1, 25000, '2025-09-15', 'especes', 'REC-001', 75000);
    """)

    _migrate_payment_modes(conn)

    assert conn.execute("SELECT mode_paiement FROM payments WHERE id = 1").fetchone()[0] == "especes"
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) "
            "VALUES (1, 25000, '2025-09-15', 'carte_bancaire', 'REC-002', 50000)"
        )
    conn.close()
