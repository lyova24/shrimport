import sys

from shrimport.config import Config, get_config


def test_config_get_from_arguments(monkeypatch):
    test_args = [
        "prog",
        "-R",
        "shrimport",
        "-i",
        "ignoreme",
        "-v",
        "-d",
        "main.py",
        "foo.py",
    ]
    monkeypatch.setattr(sys, "argv", test_args)
    config = Config.get_from_arguments()
    assert config.root_dir == "shrimport"
    assert config.is_verbose is True
    assert config.is_dry_run is True
    assert config.file_paths == ["main.py", "foo.py"]
    assert config.ignored_paths == ["ignoreme"]


def test_config_defaults(monkeypatch):
    test_args = ["prog", "main.py"]
    monkeypatch.setattr(sys, "argv", test_args)
    config = Config.get_from_arguments()
    assert config.root_dir == "."
    assert config.is_verbose is False
    assert config.is_dry_run is False
    assert config.file_paths == ["main.py"]
    assert config.ignored_paths == []


def test_get_config_lru(monkeypatch):
    test_args = ["prog", "main.py"]
    monkeypatch.setattr(sys, "argv", test_args)
    config1 = get_config()
    config2 = get_config()
    assert config1 is config2  # lru_cache returns same object
