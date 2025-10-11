from pathlib import Path
from typing import TYPE_CHECKING

import libcst

from shrimport.utils import get_module_path, make_module_attr
from shrimport.utils.code import get_code_for_node
from shrimport.utils.module import get_full_module_name

if TYPE_CHECKING:
    from pathlib import Path

    from libcst import ImportFrom


class ImportTransformer(libcst.CSTTransformer):
    def __init__(self, file_path: Path, root_dir: Path):
        super().__init__()
        self.changes: list[tuple[str, str]] = []
        self.file_path: "Path" = file_path
        self.root_dir: "Path" = root_dir
        self.modified: bool = False

    def leave_ImportFrom(
        self,
        original_node: "ImportFrom",
        updated_node: "ImportFrom",
    ) -> "ImportFrom":
        if not original_node.relative:
            return original_node

        level = len(original_node.relative) if original_node.relative else 0
        current_module = get_module_path(self.file_path, self.root_dir)
        if current_module is None:
            return original_node

        current_parts = current_module.split(".")
        if level > len(current_parts):
            print(f"warn: level {level} too deep in {self.file_path}")
            return original_node

        base_parts = current_parts[:-level]
        if original_node.module:
            module_name = get_full_module_name(original_node.module)
            full_parts = base_parts + module_name.split(".")
        else:
            full_parts = base_parts

        package_parts = current_parts[:-1]
        if full_parts[: len(package_parts)] == package_parts:
            return original_node

        new_module_str = ".".join(full_parts)
        self.modified = True
        new_node = updated_node.with_changes(
            module=make_module_attr(new_module_str),
            relative=[],
        )
        self.changes.append(
            (get_code_for_node(original_node), get_code_for_node(new_node))
        )
        return new_node
