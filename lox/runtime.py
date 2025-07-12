import builtins
from dataclasses import dataclass
from operator import add, eq, ge, gt, le, lt, mul, ne, neg, not_, sub, truediv
from typing import TYPE_CHECKING

from .ctx import Ctx

if TYPE_CHECKING:
    from .ast import Stmt, Value

__all__ = [
    "add",
    "eq",
    "ge",
    "gt",
    "le",
    "lt",
    "mul",
    "ne",
    "neg",
    "not_",
    "print",
    "show",
    "sub",
    "truthy",
    "truediv",
]


class LoxInstance:
    """
    Classe base para todos os objetos Lox.
    """

    def __str__(self):
        return f"{self.__class__.__name__} instance"


@dataclass
class LoxFunction:
    """
    Classe base para todas as funções Lox.
    """

    name: str
    args: list[str]
    body: list["Stmt"]
    ctx: Ctx

    def __call__(self, *args):
        env = dict(zip(self.args, args, strict=True))
        env = self.ctx.push(env)

        try:
            for stmt in self.body:
                stmt.eval(env)
        except LoxReturn as e:
            return e.value
    
    def __str__(self):
        return f"<fn {self.name}>"


class LoxReturn(Exception):
    """
    Exceção para retornar de uma função Lox.
    """

    def __init__(self, value):
        self.value = value
        super().__init__()


class LoxError(Exception):
    """
    Exceção para erros de execução Lox.
    """


nan = float("nan")
inf = float("inf")


def print(value: "Value"):
    """
    Imprime um valor lox.
    """
    builtins.print(show(value))


def show(value: "Value") -> str:
    """
    Converte valor lox para string.
    """


    if str(value) == "True" or str(value) == "False":
        return "true" if truthy(value) else "false"

    if isinstance(value, float):
        return str(value).removesuffix(".0")

    if isinstance(value, type(None)):
        return "nil"

    return str(value)


def show_repr(value: "Value") -> str:
    """
    Mostra um valor lox, mas coloca aspas em strings.
    """
    if isinstance(value, str):
        return f'"{value}"'
    return show(value)


def truthy(value: "Value") -> bool:
    """
    Converte valor lox para booleano segundo a semântica do lox.
    """
    if value is None or value is False:
        return False
    return True
