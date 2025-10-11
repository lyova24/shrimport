import logging

from shrimport.logger import get_logger


def test_get_logger_sets_level(monkeypatch):
    class DummyConfig:
        is_verbose = True

    monkeypatch.setattr("shrimport.logger.get_config", lambda: DummyConfig())
    logger = get_logger()
    assert logger.level == logging.DEBUG

    DummyConfig.is_verbose = False
    logger = get_logger()
    assert logger.level == logging.INFO


def test_get_logger_output(monkeypatch, capsys):
    class DummyConfig:
        is_verbose = False

    monkeypatch.setattr("shrimport.logger.get_config", lambda: DummyConfig())
    logger = get_logger()
    logger.info("hello world")
    captured = capsys.readouterr()
    assert "hello world" in captured.out
