from . import ast

class ConstantPropagation:
    def __init__(self):
        self.constants = {}

    def get_constant(self, name: str):
        return self.constants.get(name)

    def set_constant(self, name: str, value: int | float):
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
                return self.get_constant(node.name)
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