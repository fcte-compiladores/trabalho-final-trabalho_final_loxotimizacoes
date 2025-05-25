"""
Implementa o transformador da árvore sintática que converte entre as representações

    lark.Tree -> lox.ast.Node.

A resolução de vários exercícios requer a modificação ou implementação de vários
métodos desta classe.
"""

from typing import Callable
from lark import Transformer, v_args

from . import runtime as op
from .ast import *
from pprint import pprint


def op_handler(op: Callable):
    """
    Fábrica de métodos que lidam com operações binárias na árvore sintática.

    Recebe a função que implementa a operação em tempo de execução.
    """

    def method(self, left, right):
        return BinOp(left, right, op)

    return method


@v_args(inline=True)
class LoxTransformer(Transformer):
    # Programa
    def program(self, *stmts):
        return Program(list(stmts))

    # Operações matemáticas básicas
    mul = op_handler(op.mul)
    div = op_handler(op.truediv)
    sub = op_handler(op.sub)
    add = op_handler(op.add)

    # Comparações
    gt = op_handler(op.gt)
    lt = op_handler(op.lt)
    ge = op_handler(op.ge)
    le = op_handler(op.le)
    eq = op_handler(op.eq)
    ne = op_handler(op.ne)

    # Outras expressões
    def call(self, node: Var | Getattr, args: list=[]):
        return Call(node, args)
        
    def args(self, *args):
        params = list(args)
        return params
    
    def getattr_(self, obj: Call, name: Var):
        if isinstance(name, Var):
            name = name.name
        elif hasattr(name, "value"):
            name = name.value
        
        return Getattr(obj, name)

    def setattr_(self, obj: Call, name: Var, value: Expr):
        if isinstance(name, Var):
            name = name.name
        elif hasattr(name, "value"):
            name = name.value

        return Setattr(obj, name, value)

    def not_(self, expr: Expr):
        return UnaryOp(op.not_, expr)
    
    def neg(self, expr: Expr):
        return UnaryOp(op.neg, expr)
    
    def logic_or(self, *args: list[Expr]):
        return Or(args)
    
    def logic_and(self, *args: list[Expr]):
        return And(args)
    
    def decl(self, name: Var, expr: Expr):
        return VarDef(name, expr)
    
    def assign(self, name: Var, expr: Expr):
        return Assign(name, expr)


    # Comandos
    def print_cmd(self, expr):
        return Print(expr)

    def VAR(self, token):
        name = str(token)
        return Var(name)

    def NUMBER(self, token):
        num = float(token)
        return Literal(num)
    
    def STRING(self, token):
        text = str(token)[1:-1]
        return Literal(text)
    
    def NIL(self, _):
        return Literal(None)

    def BOOL(self, token):
        return Literal(token == "true")
    