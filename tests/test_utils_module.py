import libcst as cst

from src.utils.module import get_full_module_name, make_module_attr


def test_make_module_attr_none():
    assert make_module_attr(None) is None
    assert make_module_attr("") is None


def test_make_module_attr_simple():
    expr = make_module_attr("foo")
    assert isinstance(expr, cst.Name)
    assert expr.value == "foo"


def test_make_module_attr_nested():
    expr = make_module_attr("foo.bar.baz")
    assert isinstance(expr, cst.Attribute)
    assert expr.attr.value == "baz"
    assert isinstance(expr.value, cst.Attribute)
    assert expr.value.attr.value == "bar"
    assert isinstance(expr.value.value, cst.Name)
    assert expr.value.value.value == "foo"


def test_get_full_module_name_name():
    node = cst.Name("foo")
    assert get_full_module_name(node) == "foo"


def test_get_full_module_name_attribute():
    node = cst.Attribute(
        value=cst.Attribute(value=cst.Name("foo"), attr=cst.Name("bar")),
        attr=cst.Name("baz"),
    )
    assert get_full_module_name(node) == "foo.bar.baz"
