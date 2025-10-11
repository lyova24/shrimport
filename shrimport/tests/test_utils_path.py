from pathlib import Path

import pytest

from shrimport.utils.path import (
    exit_if_path_is_not_a_dir,
    get_module_path,
    get_path_from_str,
    get_paths_from_list,
)


def test_get_path_from_str(tmp_path):
    p = get_path_from_str(str(tmp_path))
    assert isinstance(p, Path)
    assert p == tmp_path.resolve()


def test_get_paths_from_list(tmp_path):
    files = [tmp_path / f"f{i}.py" for i in range(3)]
    for f in files:
        f.write_text("x")
    paths = get_paths_from_list([str(f) for f in files])
    assert all(isinstance(p, Path) for p in paths)
    assert set(paths) == set(f.resolve() for f in files)


def test_get_module_path_relative(tmp_path):
    root = tmp_path / "shrimport"
    root.mkdir()
    file = root / "pkg" / "mod.py"
    file.parent.mkdir(parents=True)
    file.write_text("x")
    module_path = get_module_path(file, root)
    assert module_path == "pkg.mod"


def test_get_module_path_not_in_root(tmp_path, capsys):
    root = tmp_path / "shrimport"
    root.mkdir()
    file = tmp_path / "other.py"
    file.write_text("x")
    result = get_module_path(file, root)
    captured = capsys.readouterr()
    assert result is None
    assert "skip:" in captured.out


def test_exit_if_path_is_not_a_dir(tmp_path):
    file = tmp_path / "f.txt"
    file.write_text("x")
    with pytest.raises(SystemExit):
        exit_if_path_is_not_a_dir(file)
    # Should not raise if dir
    exit_if_path_is_not_a_dir(tmp_path)
