import os
import sqlite3
import subprocess
import time
from pathlib import Path

import pytest


@pytest.mark.skipif(not os.environ.get("EDUPAIE_EXE"), reason="Requires the packaged Windows executable")
def test_packaged_app_starts_without_python_and_preserves_user_data(tmp_path):
    if os.name != "nt":
        pytest.skip("The packaged executable is a Windows application")

    exe_path = Path(os.environ["EDUPAIE_EXE"]).resolve()
    profile = tmp_path / "profile"
    profile.mkdir()
    local_app_data = profile / "AppData" / "Local"
    database_path = local_app_data / "EduPaie" / "edupaie.db"
    env = os.environ.copy()
    env.update(
        {
            "USERPROFILE": str(profile),
            "HOME": str(profile),
            "LOCALAPPDATA": str(local_app_data),
            "PATH": str(Path(os.environ["SystemRoot"]) / "System32"),
            "QT_QPA_PLATFORM": "offscreen",
        }
    )
    for name in ("PYTHONHOME", "PYTHONPATH", "VIRTUAL_ENV"):
        env.pop(name, None)

    taskkill = Path(os.environ["SystemRoot"]) / "System32" / "taskkill.exe"

    def launch_and_read_student_count():
        process = subprocess.Popen(
            [str(exe_path)],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            deadline = time.monotonic() + 60
            while not database_path.is_file() and time.monotonic() < deadline:
                if process.poll() is not None:
                    pytest.fail(f"EduPaie exited before creating its database (code {process.returncode})")
                time.sleep(0.2)

            assert database_path.is_file(), "EduPaie did not create its user database"
            assert process.poll() is None, "EduPaie exited during startup"
            with sqlite3.connect(database_path) as connection:
                assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                return connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        finally:
            subprocess.run(
                [str(taskkill), "/PID", str(process.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            process.wait(timeout=10)

    assert launch_and_read_student_count() == 0

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """INSERT INTO students (nom, prenom, classe, annee_scolaire, total_du)
               VALUES ('Smoke', 'Test', '6e A', '2026-2027', 12345)"""
        )

    assert launch_and_read_student_count() == 1