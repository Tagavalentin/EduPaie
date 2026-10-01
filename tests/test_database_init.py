import sqlite3
from pathlib import Path

import pytest

from src.database import init_db


@pytest.fixture
def database_path(tmp_path, monkeypatch):
    db_path = tmp_path / "edupaie.db"
    project_root = Path(__file__).resolve().parents[1]

    monkeypatch.setattr(init_db, "get_base_path", lambda: project_root)
    monkeypatch.setattr(init_db, "get_connection", lambda: sqlite3.connect(db_path))
    monkeypatch.setattr("src.utils.paths.get_db_path", lambda: db_path)
    return db_path


def test_init_database_does_not_insert_demo_data_by_default(database_path):
    init_db.init_database()

    with sqlite3.connect(database_path) as conn:
        student_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    assert student_count == 0


def test_init_database_can_insert_demo_data_when_requested(database_path):
    init_db.init_database(include_demo_data=True)

    with sqlite3.connect(database_path) as conn:
        student_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    assert student_count == 15