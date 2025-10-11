import libcst


def make_module_attr(module_path: str | None) -> libcst.BaseExpression | None:
    if not module_path:
        return None
    parts = module_path.split(".")
    expr: libcst.BaseExpression = libcst.Name(parts[0])
    for part in parts[1:]:
        expr = libcst.Attribute(value=expr, attr=libcst.Name(part))
    return expr


def get_full_module_name(module_node: libcst.BaseExpression) -> str:
    if isinstance(module_node, libcst.Name):
        return module_node.value
    elif isinstance(module_node, libcst.Attribute):
        return get_full_module_name(module_node.value) + "." + module_node.attr.value
    else:
        return ""
