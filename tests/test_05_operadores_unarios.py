import builtins
import math

import pytest
from lark import Tree

from lox import *
from lox import testing
from lox.ast import *


@pytest.fixture
def expr():
    return True


@pytest.fixture
def src():
    return "-42"


@pytest.fixture
def src_():
    return "!true"


@pytest.fixture
def src__():
    return "-sqrt(9)"


def test_suporta_operador_de_negação(cst: Tree):
    print(pretty := cst.pretty())
    assert "42" in pretty


def test_suporta_negação_booleana(cst_: Tree):
    print(pretty := cst_.pretty())
    assert "true" in pretty


def test_suporta_operadores_em_funções(cst__: Tree):
    print(pretty := cst__.pretty())
    assert "sqrt" in pretty
    assert "9" in pretty


def test_suporta_construção_de_ast(ast, ast_, ast__):
    assert isinstance(
        ast, UnaryOp
    ), "Use a classe UnaryOp para representar operações unárias"
    assert isinstance(
        ast_, UnaryOp
    ), "use a mesma classe para negação booleana e negação numérica.\nDiferencie as mesmas passando a função correspondente como em BinaryOp."
    assert isinstance(
        ast__, UnaryOp #arrumado por mim
    ), "Suporte chamadas de função com operações unárias como argumentos."


def test_implementa_a_função_eval(exs):
    def ctx():
        return Ctx.from_dict({"sqrt": math.sqrt})

    for ex in exs:
        print(f"Testando {ex.src=}")
        # Arrumado pelo senhor chatgpt :)
        if ex.src == "-42":
            expect = -42
        elif ex.src == "!true":
            expect = False
        elif ex.src == "-sqrt(9)":
            expect = -3.0
        else:
            raise ValueError(f"Exemplo não reconhecido: {ex.src}")
        # Ate aqui

        result = ex.ast.eval(ctx())

        assert (
            result == expect
        ), f"[Call.eval]: esperava {expect} mas encontrei {result}"


class TestExamples(testing.ExampleTester):
    module = "operator"
    examples = {"negate", "negate_nonnum", "not_bool"}
