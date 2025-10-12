import os
from re import compile
from typing import TYPE_CHECKING

import libcst as cst

from shrimport.config import Config
from shrimport.constants import DEFAULT_TEXT_ENCODING, PYTHON_FILE_EXTENSION
from shrimport.logger import get_logger
from shrimport.utils import (
    exit_if_path_is_not_a_dir,
    get_path_from_str,
    get_paths_from_list,
)

from .import_transformer import ImportTransformer

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Pattern

    from shrimport.logger import ShrimportLogger


class ImportFormatter:
    def __init__(self, config: Config):
        self.logger: "ShrimportLogger" = get_logger()
        self.root_dir: "Path" = get_path_from_str(config.root_dir).resolve()
        self.file_paths: list["Path"] = get_paths_from_list(config.file_paths)
        self.ignore_patterns: list["Pattern"] = list(
            set([compile(pattern) for pattern in config.ignored_paths])
        )
        self.is_dry_run: bool = config.is_dry_run
        exit_if_path_is_not_a_dir(self.root_dir)

    def convert_relative_imports(self) -> int:
        exit_code = os.EX_OK
        scanned, changed = 0, 0
        for file_path in self.file_paths:
            if (
                not file_path.is_file()
                or not file_path.name.endswith(PYTHON_FILE_EXTENSION)
                or any(pat.search(str(file_path)) for pat in self.ignore_patterns)
            ):
                self.logger.log_ignored(file_path)
                continue

            scanned += 1
            if self._convert_imports(file_path):
                exit_code = os.EX_DATAERR
                changed += 1
        return exit_code

    def _convert_imports(self, file_path: "Path") -> bool:
        source = file_path.read_text(encoding=DEFAULT_TEXT_ENCODING)
        tree = cst.parse_module(source)

        transformer = ImportTransformer(file_path, self.root_dir)
        modified_tree = tree.visit(transformer)

        if transformer.modified:
            if self.is_dry_run:
                self.logger.log_disapproved(file_path=file_path)
            else:
                self.logger.log_file_changed(file_path=file_path)
                file_path.write_text(modified_tree.code, encoding=DEFAULT_TEXT_ENCODING)
            for change in transformer.changes:
                self.logger.log_changes(from_code=change[0], to_code=change[1])
            return True
        self.logger.log_approved(file_path)
        return False
