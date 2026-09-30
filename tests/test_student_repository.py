import sqlite3
import pytest
from datetime import datetime

from src.repositories.student_repository import StudentRepository
from src.models.student import Student


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
    # Monkeypatch pour utiliser la base en mémoire
    import src.repositories.student_repository as repo_module
    monkeypatch.setattr(repo_module, 'get_connection', lambda: in_memory_db)
    monkeypatch.setattr(repo_module, 'close_connection', lambda conn: None)
    
    return StudentRepository()


def test_create_student(repo):
    """Test la création d'un élève."""
    student = Student(
        id=None,
        nom="Dupont",
        prenom="Jean",
        classe="6ème A",
        annee_scolaire="2025-2026",
        total_du=150000
    )
    
    created = repo.create(student)
    
    assert created.id is not None
    assert created.nom == "Dupont"
    assert created.prenom == "Jean"
    assert created.classe == "6ème A"
    assert created.total_du == 150000


def test_get_by_id(repo):
    """Test la récupération d'un élève par id."""
    student = Student(
        id=None,
        nom="Martin",
        prenom="Marie",
        classe="5ème B",
        annee_scolaire="2025-2026",
        total_du=175000
    )
    created = repo.create(student)
    
    found = repo.get_by_id(created.id)
    
    assert found is not None
    assert found.id == created.id
    assert found.nom == "Martin"
    assert found.prenom == "Marie"


def test_get_by_id_not_found(repo):
    """Test la récupération d'un élève inexistant."""
    found = repo.get_by_id(999)
    assert found is None


def test_get_all(repo):
    """Test la récupération de tous les élèves."""
    repo.create(Student(None, "A", "A", "6ème A", "2025-2026", 150000))
    repo.create(Student(None, "B", "B", "6ème B", "2025-2026", 150000))
    repo.create(Student(None, "C", "C", "5ème A", "2025-2026", 175000))
    
    students = repo.get_all()
    
    assert len(students) == 3
    assert all(s.id is not None for s in students)


def test_search_by_name(repo):
    """Test la recherche par nom/prénom."""
    repo.create(Student(None, "Dupont", "Jean", "6ème A", "2025-2026", 150000))
    repo.create(Student(None, "Dupond", "Marie", "6ème B", "2025-2026", 150000))
    repo.create(Student(None, "Martin", "Paul", "5ème A", "2025-2026", 175000))
    
    results = repo.search_by_name("dup")
    
    assert len(results) == 2
    assert all("dup" in s.nom.lower() or "dup" in s.prenom.lower() for s in results)


def test_filter_by_class(repo):
    """Test le filtrage par classe."""
    repo.create(Student(None, "A", "A", "6ème A", "2025-2026", 150000))
    repo.create(Student(None, "B", "B", "6ème A", "2025-2026", 150000))
    repo.create(Student(None, "C", "C", "5ème A", "2025-2026", 175000))
    
    results = repo.filter_by_class("6ème A")
    
    assert len(results) == 2
    assert all(s.classe == "6ème A" for s in results)


def test_update_student(repo):
    """Test la mise à jour d'un élève."""
    student = repo.create(Student(None, "Ancien", "Nom", "6ème A", "2025-2026", 150000))
    
    student.nom = "Nouveau"
    student.prenom = "Prenom"
    student.total_du = 200000
    updated = repo.update(student)
    
    found = repo.get_by_id(student.id)
    assert found.nom == "Nouveau"
    assert found.prenom == "Prenom"
    assert found.total_du == 200000


def test_delete_student(repo):
    """Test la suppression d'un élève."""
    student = repo.create(Student(None, "A", "A", "6ème A", "2025-2026", 150000))
    
    result = repo.delete(student.id)
    
    assert result is True
    assert repo.get_by_id(student.id) is None


def test_delete_student_not_found(repo):
    """Test la suppression d'un élève inexistant."""
    result = repo.delete(999)
    assert result is False


def test_has_payments_no_payments(repo, in_memory_db):
    """Test la vérification des paiements pour un élève sans paiements."""
    student = repo.create(Student(None, "A", "A", "6ème A", "2025-2026", 150000))
    
    assert repo.has_payments(student.id) is False


def test_has_payments_with_payments(repo, in_memory_db):
    """Test la vérification des paiements pour un élève avec paiements."""
    student = repo.create(Student(None, "A", "A", "6ème A", "2025-2026", 150000))
    
    # Ajouter un paiement
    in_memory_db.execute(
        "INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES (?, ?, ?, ?, ?, ?)",
        (student.id, 50000, "2025-09-15", "especes", "REC-001", 100000)
    )
    in_memory_db.commit()
    
    assert repo.has_payments(student.id) is True
