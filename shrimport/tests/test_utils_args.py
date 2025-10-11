import sys

import pytest

from shrimport.utils.args import get_args


def test_get_args_basic(monkeypatch):
    test_args = ["prog", "file1.py", "file2.py"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = get_args()
    assert args.root_dir == "."
    assert args.ignored_paths == []
    assert args.is_verbose is False
    assert args.is_dry_run is False
    assert args.file_paths == ["file1.py", "file2.py"]


def test_get_args_with_all_options(monkeypatch):
    test_args = [
        "prog",
        "-R",
        "./shrimport",
        "-i",
        "test_ignore",
        "-i",
        "other_ignore",
        "-v",
        "-d",
        "main.py",
        "foo/bar.py",
    ]
    monkeypatch.setattr(sys, "argv", test_args)
    args = get_args()
    assert args.root_dir == "./shrimport"
    assert args.ignored_paths == ["test_ignore", "other_ignore"]
    assert args.is_verbose is True
    assert args.is_dry_run is True
    assert args.file_paths == ["main.py", "foo/bar.py"]


def test_get_args_missing_files(monkeypatch):
    test_args = ["prog"]
    monkeypatch.setattr(sys, "argv", test_args)
    with pytest.raises(SystemExit):
        get_args()
