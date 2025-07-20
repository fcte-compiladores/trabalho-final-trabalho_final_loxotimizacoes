from abc import ABC
from dataclasses import dataclass
from typing import Callable
from .ctx import Ctx
from .runtime import truthy, LoxReturn, LoxFunction, print

# Declaramos nossa classe base num módulo separado para esconder um pouco de
# Python relativamente avançado de quem não se interessar pelo assunto.
#
# A classe Node implementa um método `pretty` que imprime as árvores de forma
# legível. Também possui funcionalidades para navegar na árvore usando cursores
# e métodos de visitação.
from .node import Node


#
# TIPOS BÁSICOS
#

# Tipos de valores que podem aparecer durante a execução do programa
Value = bool | str | float | None


class Expr(Node, ABC):
    """
    Classe base para expressões.

    Expressões são nós que podem ser avaliados para produzir um valor.
    Também podem ser atribuídos a variáveis, passados como argumentos para
    funções, etc.
    """


class Stmt(Node, ABC):
    """
    Classe base para comandos.

    Comandos são associdos a construtos sintáticos que alteram o fluxo de
    execução do código ou declaram elementos como classes, funções, etc.
    """


@dataclass
class Program(Node):
    """
    Representa um programa.

    Um programa é uma lista de comandos.
    """

    stmts: list[Stmt]

    def eval(self, ctx: Ctx):
        for stmt in self.stmts:
            stmt.eval(ctx)


#
# EXPRESSÕES
#
@dataclass
class BinOp(Expr):
    """
    Uma operação infixa com dois operandos.

    Ex.: x + y, 2 * x, 3.14 > 3 and 3.14 < 4
    """

    left: Expr
    right: Expr
    op: Callable[[Value, Value], Value]

    def eval(self, ctx: Ctx):
        left_value = self.left.eval(ctx)
        right_value = self.right.eval(ctx)
        return self.op(left_value, right_value)


@dataclass
class Var(Expr):
    """
    Uma variável no código

    Ex.: x, y, z
    """

    name: str

    def eval(self, ctx: Ctx):
        try:
            return ctx.__getitem__(self.name)
        except KeyError:
            raise NameError(f"variável {self.name} não existe!")


@dataclass
class Literal(Expr):
    """
    Representa valores literais no código, ex.: strings, booleanos,
    números, etc.

    Ex.: "Hello, world!", 42, 3.14, true, nil
    """

    value: Value

    def eval(self, ctx: Ctx):
        return self.value


@dataclass
class And(Expr):
    """
    Uma operação infixa com dois operandos.

    Ex.: x and y
    """

    expr: list[Expr]

    def eval(self, ctx):
        
        first = self.expr[0].eval(ctx)

        if first == False:
            return False
        
        second = self.expr[1].eval(ctx)

        if second == False:
            return False
        
        return True


@dataclass
class Or(Expr):
    """
    Uma operação infixa com dois operandos.
    Ex.: x or y
    """
    expr: list[Expr]

    def eval(self, ctx):
        first = self.expr[0].eval(ctx)

        if first == True:
            return True
        
        second = self.expr[1].eval(ctx)

        if second == True:
            return True
        
        return False


@dataclass
class UnaryOp(Expr):
    """
    Uma operação prefixa com um operando.

    Ex.: -x, !x
    """

    op: Callable[[Value], Value]
    expr: Expr

    def eval(self, ctx: Ctx):
        value = self.expr.eval(ctx)
        return self.op(value)

@dataclass
class Call(Expr):
    """
    Uma chamada de função.

    Ex.: fat(42)
    """
    node: Expr
    args: list[Expr]
    
    def eval(self, ctx: Ctx):
        func = self.node.eval(ctx)
        args = [arg.eval(ctx) for arg in self.args]


        if callable(func):
            return func(*args)
        else:
            raise TypeError(f"{self.node.name} não é uma função!")


@dataclass
class This(Expr):
    """
    Acesso ao `this`.

    Ex.: this
    """


@dataclass
class Super(Expr):
    """
    Acesso a method ou atributo da superclasse.

    Ex.: super.x
    """


@dataclass
class Assign(Expr):
    """
    Atribuição de variável.

    Ex.: x = 42
    """
    name: Var
    expr: Expr

    def eval(self, ctx: Ctx):
        if (self.name.name in ctx):
            value = self.expr.eval(ctx)
            ctx[self.name.name] = value
            return value
        else:
            raise NameError(f"variável {self.name.name} não existe!")


@dataclass
class Getattr(Expr):
    """
    Acesso a atributo de um objeto.

    Ex.: x.y
    """
    obj: Expr
    name: str

    def eval(self, ctx: Ctx):
        obj = self.obj.eval(ctx)

        if isinstance(obj, dict):
            if self.name in obj:
                return obj[self.name]
            raise AttributeError(f"Atributo {self.name} não encontrado no objeto {type(obj).__name__}")
        
        if hasattr(obj, self.name):
            return getattr(obj, self.name)
        raise TypeError(f"Não é um objeto")


@dataclass
class Setattr(Expr):
    """
    Atribuição de atributo de um objeto.

    Ex.: x.y = 42
    """

    obj: Expr
    name: str
    value: Expr

    def eval(self, ctx: Ctx):
        obj = self.obj.eval(ctx)

        if (hasattr(obj, self.name)):
            value = self.value.eval(ctx)
            setattr(obj, self.name, value)
            return value

        raise AttributeError(f"Atributo {self.name} não encontrado no objeto {type(obj).__name__}")


#
# COMANDOS
#
@dataclass
class Print(Stmt):
    """
    Representa uma instrução de impressão.

    Ex.: print "Hello, world!";
    """
    expr: Expr
    
    def eval(self, ctx: Ctx):
        value = self.expr.eval(ctx)
        print(value)


@dataclass
class Return(Stmt):
    """
    Representa uma instrução de retorno.

    Ex.: return x;
    """

    expr: Expr

    def eval(self, ctx): 
        raise LoxReturn(self.expr.eval(ctx))


@dataclass
class VarDef(Stmt):
    """
    Representa uma declaração de variável.

    Ex.: var x = 42;
    """

    name: str
    expr: Expr

    def eval(self, ctx: Ctx):
        value = self.expr.eval(ctx)
        ctx.var_def(self.name, value)


@dataclass
class If(Stmt):
    """
    Representa uma instrução condicional.

    Ex.: if (x > 0) { ... } else { ... }
    """

    cond: Expr
    then: Expr
    not_then: Expr
    
    def eval(self, ctx: Ctx):
        if(truthy(self.cond.eval(ctx))):
            self.then.eval(ctx)
        else:
            self.not_then.eval(ctx)


@dataclass
class While(Stmt):
    """
    Representa um laço de repetição.

    Ex.: while (x > 0) { ... }
    """

    cond: Expr
    then: Expr

    def eval(self, ctx: Ctx):
        cond = self.cond.eval(ctx)
        
        if (truthy(cond)):
            self.then.eval(ctx)
            self.eval(ctx)
        


@dataclass
class Block(Node):
    """
    Representa bloco de comandos.

    Ex.: { var x = 42; print x;  }
    """

    statements: list[Stmt]

    def eval(self, ctx: Ctx):
        ctx = ctx.push({}) 
        for stmt in self.statements:
            stmt.eval(ctx)

@dataclass
class Function(Stmt):
    """
    Representa uma função.

    Ex.: fun f(x, y) { ... }
    """

    identifier: str
    args: list[str]
    body: Expr

    def eval(self, ctx: Ctx):
        loxFn = LoxFunction(
            name=self.identifier,
            args=self.args,
            body=[self.body],
            ctx=ctx
        )

        ctx.var_def(self.identifier, loxFn)
        return loxFn


@dataclass
class Class(Stmt):
    """
    Representa uma classe.

    Ex.: class B < A { ... }
    """

@dataclass
class NoOp(Stmt):
    """
    Representa uma instrução vazia.

    Ex.: ;
    """

    noop: bool = True # TODO: remover isso, coloquei por que se não tiver argumentos da erro no node algo com __annotations__

    def eval(self, ctx: Ctx):
        pass