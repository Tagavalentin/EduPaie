from pathlib import Path

from src.utils import paths


def test_frozen_app_uses_local_appdata_for_data(monkeypatch, tmp_path):
    local_app_data = tmp_path / "LocalAppData"
    monkeypatch.setattr(paths.sys, "frozen", True, raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))

    data_path = paths.get_data_path()

    assert data_path == local_app_data / "EduPaie"
    assert data_path.is_dir()