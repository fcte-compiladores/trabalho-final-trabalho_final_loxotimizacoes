from . import ast
from typing import Callable
class ConstantPropagation:
    def __init__(self):
        self.constants = {}

    def get_constant(self, name: str):
        return self.constants.get(name)

    def set_constant(self, name: str, value: int | float):
        if value is None or value is False:
            return
        self.constants[name] = value

    def propagate(self, node: ast.Expr) -> ast.Expr:
        if isinstance(node, ast.BinOp):
            left = self.propagate(node.left)
            right = self.propagate(node.right)
            if (isinstance(left, ast.Literal) and isinstance(right, ast.Literal)):
                return ast.Literal(node.op(left.value, right.value))
        elif isinstance(node, ast.VarDef):
            initializer = self.propagate(node.expr)
            
            if isinstance(initializer, ast.Literal):
                self.set_constant(node.name, ast.Literal(initializer.value))
                return ast.VarDef(name=node.name, expr=initializer)
            
            return node
        elif isinstance(node, ast.Function):
            # Não é seguro propagar funções por causa de efeitos colaterais...
            return node

        elif isinstance(node, ast.Call):
            node.args = [self.propagate(arg) for arg in node.args]
            return node

        elif isinstance(node, ast.Var):
            if (node.name in self.constants):
                return self.get_constant(node.name)
            return node
        elif isinstance(node, ast.Block):
            old_body = self.constants.copy()
            node.statements = [self.propagate(stmt) for stmt in node.statements]
            self.constants = old_body
            return node
        else:
            return loop_ast_nodes(node, self.propagate)

            
class UnsedVarsElimination:
    def __init__(self):
        self.used_vars = set()
    
    def mark_used(self, name: str):
        self.used_vars.add(name)
    
    def is_used(self, name: str) -> bool:
        return name in self.used_vars
    
    def evaluate_used_vars(self, node: ast.Expr) -> ast.Expr:
        if isinstance(node, ast.VarDef):
            node.expr = self.evaluate_used_vars(node.expr)
            return node
        
        if isinstance(node, ast.Function):
            self.mark_used(node.identifier)
            self.evaluate_used_vars(node.body)
            return node
        
        if isinstance(node, ast.Var):
            self.mark_used(node.name)
            return node
        
        if isinstance(node, ast.BinOp):
            node.left = self.evaluate_used_vars(node.left)
            node.right = self.evaluate_used_vars(node.right)
            return node
        
        if isinstance(node, ast.Block):
            old_used_vars = self.used_vars.copy()
            node.statements = [self.evaluate_used_vars(stmt) for stmt in node.statements]
            self.used_vars = old_used_vars
            return node
        else:
            return loop_ast_nodes(node, self.evaluate_used_vars)
        
    def remove_unused_vars(self, node: ast.Expr) -> ast.Expr:
        if isinstance(node, ast.VarDef):
            if not self.is_used(node.name):
                return ast.NoOp()
            node.expr = self.remove_unused_vars(node.expr)
            return node
        return loop_ast_nodes(node, self.remove_unused_vars)
    def eval(self, program: ast.Program) -> ast.Program:
        self.evaluate_used_vars(program)
        return self.remove_unused_vars(program)


def optimize_ast(ast_program: ast.Expr, optimizations: list = ['propagation', 'unsed_vars']) -> ast.Expr:
    """
    Otimiza a AST

    Aplicando as seguintes otimizações:
    - constant propagation
    - constant folding
    - unsed variable elimination

    o segundo parâmetro `optimizations` é uma lista de strings que especifica quais otimizações aplicar.
    optimizations: ['propagation', 'unsed_vars']
    """
    optimizer = ast_program
   
    if 'propagation' in optimizations:
        ConstantPropagation().propagate(optimizer)
    if 'unsed_vars' in optimizations:
        UnsedVarsElimination().eval(optimizer) 
    
    return ast_program



def loop_ast_nodes(node: ast.Expr, callback: Callable[[ast.Expr], ast.Expr]) -> ast.Expr:
    if isinstance(node, str):
        return node
    for attr, value in vars(node).items():
        if isinstance(value, list):
            setattr(node, attr, [callback(item) for item in value])
        elif isinstance(value, ast.Expr):
            setattr(node, attr, callback(value))
    return node