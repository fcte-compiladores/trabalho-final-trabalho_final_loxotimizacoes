import builtins
from dataclasses import dataclass
from operator import add, eq, ge, gt, le, lt, mul, ne, neg, not_, sub, truediv
from typing import TYPE_CHECKING
from . import ast

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



class ConstantPropagation:
    def __init__(self):
        self.constants = {}

    def get_constant(self, name: str):
        return self.constants.get(name)

    def set_constant(self, name: str, value: "Value"):
        if value is None or value is False:
            return
        self.constants[name] = value

    def propagate(self, node: "ast.Expr") -> "ast.Expr":
        if isinstance(node, ast.BinOp):
            left = self.propagate(node.left)
            right = self.propagate(node.right)
            if (isinstance(left, ast.Literal) and isinstance(right, ast.Literal)):
                return ast.Literal(self.eval_propagation(node.op, left.value, right.value))
        elif isinstance(node, ast.VarDef):
            initializer = self.propagate(node.expr)
            
            if isinstance(initializer, ast.Literal):
                self.set_constant(node.var.name, ast.Literal(initializer.value))
                return ast.VarDef(var=node.var, expr=initializer) 
            
            return node
        
        elif isinstance(node, ast.Var):
            if (node.name in self.constants):
                return self.constants[node.name]
            return node
        elif isinstance(node, ast.Block):
            old_body = self.constants.copy()
            node.statements = [self.propagate(stmt) for stmt in node.statements]
            self.constants = old_body
            return node
        else:
            for attr, value in vars(node).items():
                if isinstance(value, list):
                    setattr(node, attr, [self.propagate(item) for item in value])
                elif isinstance(value, ast.Expr):
                    setattr(node, attr, self.propagate(value))
            return node
            
    def eval_propagation(self, operator, left, right):
        return operator(left, right)
