from lox import optimizations, parse
from configs import pretty_test, load_examples, print_benchmark
from rich import print
import sys
import shutil
import copy

"""

Instruções:

Rode esse arquivo com `uv run tests/optimization.py`
Após isso ele criará um arquivo results.txt na pasta tests com o resultado das otimizações.

Acesse o arquivo com `less -R tests/results.txt` para ver o resultado das otimizações.
NOTE: Abrir o arquivo TXT haverá problemas com as cores ANSI, use o less com a opção -R para ver as cores corretamente.

"""


def test_constant_and_folding_ast(src: str, ast_program=None):
  original_ast = copy.deepcopy(ast_program) if ast_program else parse(src)
  if ast_program is None:
    ast_program = parse(src)
  print(f"[red][bold][FOLDING + PROPAGATION][/bold] - AST Original:[/red]\n{ast_program.pretty()}")


  optimizations.optimize_ast(ast_program, optimizations=["propagation"])

  print(f"[cyan][bold][FOLDING + PROPAGATION][/bold] - AST Optimized:[/cyan]\n{ast_program.pretty()}")
  return [ast_program, original_ast]


def test_unsed_vars(src: str, ast_program=None):
  original_ast = copy.deepcopy(ast_program) if ast_program else parse(src)
  if ast_program is None:
    ast_program = parse(src)
  print(f"[red][bold][UNSED VARS][/bold] - AST Original:[/red]\n{ast_program.pretty()}")
  optimizations.optimize_ast(ast_program, optimizations=["unsed_vars"])
  
  print(f"[cyan][bold][UNSED VARS][/bold] - AST Optimized:[/cyan]\n{ast_program.pretty()}")
  return [ast_program, original_ast]


def print_divider(char='-'):
    width = shutil.get_terminal_size().columns
    print(char * width)

def test(tests):
  with open("tests/results.txt", "w"):
    pass
  for [index, test] in enumerate(tests, start=1):
      print (f"Testing source: {test['relative_path']}")
      with open("tests/results.txt", "a") as f:
          sys.stdout = f
          print_divider()
          print(pretty_test(test, index))

          ast, original_ast = [None, None]
          if "propagation" in test["optimizations"]:
            ast, original_ast = test_constant_and_folding_ast(test["src"])
          if "unsed_vars" in test["optimizations"]:
            ast, original_ast = test_unsed_vars(test["src"], ast)

          print_benchmark(test, original_ast, ast)
          sys.stdout = sys.__stdout__
  print (f"[bold][green]Tests completed![/green][/bold]")
  print (f"[bold]Run following command to view results:[/bold]")
  print (f"[blue]less -R tests/results.txt[/blue]")

test(load_examples())