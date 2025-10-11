import logging
import sys
from enum import StrEnum
from typing import TYPE_CHECKING

from src.config import get_config

if TYPE_CHECKING:
    from pathlib import Path


class LogColor(StrEnum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"  # Used to reset color change


class ShrimportLogger(logging.Logger):
    def __init__(self, name: str, level: int = logging.NOTSET) -> None:
        super().__init__(name=name, level=level)

    def log_approved(self, file_path: "Path") -> None:
        self._log(
            level=logging.DEBUG,
            msg=f"{LogColor.BLUE}Approved:{LogColor.RESET} {file_path}",
            args=(),
        )

    def log_changes(self, from_code: str, to_code: str) -> None:
        self._log(
            level=logging.WARNING,
            msg=f"\t{LogColor.RED}{from_code}{LogColor.RESET} -> {LogColor.GREEN}{to_code}{LogColor.RESET}",
            args=(),
        )

    def log_file_changed(self, file_path: "Path") -> None:
        self._log(
            level=logging.WARNING,
            msg=f"{LogColor.YELLOW}Changed:{LogColor.RESET} {file_path}",
            args=(),
        )

    def log_disapproved(self, file_path: "Path") -> None:
        self._log(
            level=logging.WARNING,
            msg=f"{LogColor.YELLOW}Disapproved:{LogColor.RESET} {file_path}",
            args=(),
        )

    def log_ignored(self, file_path: "Path") -> None:
        self._log(
            level=logging.WARNING,
            msg=f"Ignored: {file_path}",
            args=(),
        )


def get_logger(name: str = __name__) -> ShrimportLogger:
    config = get_config()
    formatter = logging.Formatter("%(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO if not config.is_verbose else logging.DEBUG)
    handler.setFormatter(formatter)

    log = ShrimportLogger(name=name)
    log.addHandler(handler)
    log.setLevel(handler.level)
    return log
