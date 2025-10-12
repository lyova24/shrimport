import libcst as cst

from shrimport.service.import_transformer import ImportTransformer


def make_tree(source):
    return cst.parse_module(source)


def test_leave_importfrom_absolute(tmp_path):
    file_path = tmp_path / "pkg" / "mod.py"
    root_dir = tmp_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("x")
    transformer = ImportTransformer(file_path, root_dir)
    node = cst.ImportFrom(
        module=cst.Name("os"),
        names=[cst.ImportAlias(name=cst.Name("path"))],
        relative=[],
    )
    result = transformer.leave_ImportFrom(node, node)
    assert result is node
    assert transformer.modified is False


def test_leave_importfrom_relative(tmp_path):
    file_path = tmp_path / "pkg" / "mod.py"
    root_dir = tmp_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("x")
    transformer = ImportTransformer(file_path, root_dir)
    node = cst.ImportFrom(
        module=cst.Name("foo"),
        names=[cst.ImportAlias(name=cst.Name("bar"))],
        relative=[cst.Dot()],
    )
    updated_node = node.with_changes()
    result = transformer.leave_ImportFrom(node, updated_node)
    assert result is node


def test_leave_importfrom_too_deep(tmp_path):
    file_path = tmp_path / "pkg" / "mod.py"
    root_dir = tmp_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("x")
    transformer = ImportTransformer(file_path, root_dir)
    node = cst.ImportFrom(
        module=None,
        names=[cst.ImportAlias(name=cst.Name("bar"))],
        relative=[cst.Dot(), cst.Dot(), cst.Dot()],
    )
    updated_node = node.with_changes()
    result = transformer.leave_ImportFrom(node, updated_node)
    assert result is node
