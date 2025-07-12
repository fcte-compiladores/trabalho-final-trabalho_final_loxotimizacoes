from lox import ast
from lox import runtime
from lox import parse
from rich import print

def test(src: str):
  ast_program = parse(src)
  print(f"Original: {ast_program.pretty()}")
  runtime.ConstantPropagation().propagate(ast_program)
  print(f"Optimized: {ast_program.pretty()}")

def test_unreach(src: str):
   ast_program = parse(src)
   print(f"Original: {ast_program.pretty()}")
   runtime.UnreachableCodeOptimization().optimize(ast_program)
   print(f"Optimized: {ast_program.pretty()}")



src1_simple = """
var x = 1;
var y = 1 + x; // expect to perform 1 + 1 then folding and y = 2;
"""

srcs = [
  src1,
  # src2,
  # src3,
]


for src in srcs:
    print (f"Testing source:\n{src}")
    test(src)


