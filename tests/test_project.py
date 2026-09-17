from pathlib import Path


def test_expected_project_directories_exist() -> None:
    for directory in ("configs", "data", "models", "notebooks", "outputs", "reports", "scripts", "src"):
        assert Path(directory).is_dir()

