from pathlib import Path

from shrimport.config import Config
from shrimport.service.import_formatter import ImportFormatter


def make_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_import_formatter_dry_run(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    file1 = pkg / "mod.py"
    file2 = pkg / "other.py"
    make_file(file1, "from .foo import bar\n")
    make_file(file2, "print('hello')\n")
    config = Config(
        root_dir=str(tmp_path),
        is_verbose=True,
        is_dry_run=True,
        file_paths=[str(file1), str(file2)],
        ignored_paths=[],
    )
    formatter = ImportFormatter(config)
    exit_code = formatter.convert_relative_imports()
    assert exit_code == 0


def test_import_formatter_real_run(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    file1 = pkg / "mod.py"
    make_file(file1, "from .foo import bar\n")
    config = Config(
        root_dir=str(tmp_path),
        is_verbose=True,
        is_dry_run=False,
        file_paths=[str(file1)],
        ignored_paths=[],
    )
    formatter = ImportFormatter(config)
    exit_code = formatter.convert_relative_imports()
    assert exit_code == 0
    content = file1.read_text(encoding="utf-8")
    assert "from .foo import bar" in content


def test_import_formatter_ignores_non_py(tmp_path):
    file1 = tmp_path / "a.txt"
    make_file(file1, "from .foo import bar\n")
    config = Config(
        root_dir=str(tmp_path),
        is_verbose=True,
        is_dry_run=False,
        file_paths=[str(file1)],
        ignored_paths=[],
    )
    formatter = ImportFormatter(config)
    exit_code = formatter.convert_relative_imports()
    assert exit_code == 0


def test_import_formatter_ignores_by_pattern(tmp_path):
    file1 = tmp_path / "skip_me.py"
    make_file(file1, "from .foo import bar\n")
    config = Config(
        root_dir=str(tmp_path),
        is_verbose=True,
        is_dry_run=False,
        file_paths=[str(file1)],
        ignored_paths=["skip_me"],
    )
    formatter = ImportFormatter(config)
    exit_code = formatter.convert_relative_imports()
    assert exit_code == 0
