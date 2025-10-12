from typing import TYPE_CHECKING

from libcst import Module

from shrimport.constants import DEFAULT_NODE_CODE_LENGTH

if TYPE_CHECKING:
    from libcst import ImportFrom


def get_code_for_node(
    node: "ImportFrom", limit: int | None = DEFAULT_NODE_CODE_LENGTH
) -> str:
    """Returns code for ImportFrom node limited by length."""

    code = Module([]).code_for_node(node).strip()
    if limit is not None and len(code) > limit:
        code = f"{code[:limit].strip()}..."
    return code
