import pytest
from lox import Ctx

# lox/test_ctx.py

def test_getitem_current_scope():
    ctx = Ctx()
    ctx.var_def("x", 42)
    assert ctx["x"] == 42
    assert ctx.access_count["x"] == 1

def test_getitem_parent_scope():
    parent_ctx = Ctx()
    parent_ctx.var_def("y", 99)
    child_ctx = Ctx(parent=parent_ctx)
    assert child_ctx["y"] == 99
    assert parent_ctx.access_count["y"] == 1

def test_getitem_variable_not_found():
    ctx = Ctx()
    with pytest.raises(KeyError, match="Variable 'z' not found in context."):
        _ = ctx["z"]

def test_getitem_access_count_increment():
    ctx = Ctx()
    ctx.var_def("a", 10)
    _ = ctx["a"]
    _ = ctx["a"]
    assert ctx.access_count["a"] == 2


def test_cleanup_unsed_vars():
    ctx = Ctx()
    ctx.var_def("b", 20)
    ctx.var_def("c", 30)
    ctx.cleanup_unsed_vars()
    assert "b" not in ctx.scope
    assert "c" not in ctx.scope

def test_cleanup_unsed_vars_no_change():
    ctx = Ctx()
    ctx.var_def("d", 40)
    _ = ctx["d"]
    ctx.cleanup_unsed_vars()
    assert "d" in ctx.scope