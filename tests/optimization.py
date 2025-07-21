from lox import optimizations, parse
from .configs import pretty_test, load_examples, print_benchmark, BASE_DIR, parse_file_metadata
from rich import print
import sys
import shutil
import copy
import argparse


"""

Instruções:

Rode esse arquivo com `uv run tests/optimization.py`
Após isso ele criará um arquivo results.txt na pasta tests com o resultado das otimizações.

Acesse o arquivo com `less -R tests/results.txt` para ver o resultado das otimizações.
NOTE: Abrir o arquivo TXT haverá problemas com as cores ANSI, use o less com a opção -R para ver as cores corretamente.

"""


def make_argparser():
  parser = argparse.ArgumentParser(description="Testes de otimização do Lox")
  parser.add_argument(
    "file",
    nargs="?",
    default="all",
    help="Arquivo de entrada com os testes de otimização.",
  )

  parser.add_argument(
    "-p",
    "--print",
    action="store_true",
    help="Imprime o resultado dos testes no terminal.",
  )
  
  parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="tests/results.txt",
    help="Arquivo de saída para os resultados dos testes.",
  )

  parser.add_argument(
    '-b',
    '--benchmark',
    type=str,
    choices=["true", "false"],
    default="true",
    help="Habilita o benchmark dos testes de otimização.",
  )

  return parser


def main():
  parser = make_argparser()
  args = parser.parse_args()
  tests = []
  
  if (args.file == "all"):
    tests = load_examples()
  else:
    path = BASE_DIR.joinpath(args.file)
    try:
      with open(path, "r") as f:
        src = f.read()
        metadata = parse_file_metadata(src, path)
        tests.append(metadata)        
    except FileNotFoundError:
      print(f"Arquivo {args.file} não encontrado.")
      exit(1)

  if not tests:
    print(f"Nenhum teste encontrado no arquivo {args.file}.")
    exit(1)
  
   
  test(tests, print_results=args.print, output_file=args.output, benchmark=args.benchmark == "true")
  

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

    
def print_test(test: dict, index: int, benchmark: bool = True):
  print_divider()
  print(pretty_test(test, index))

  ast, original_ast = [None, None]
  if "propagation" in test["optimizations"]:
    ast, original_ast = test_constant_and_folding_ast(test["src"])
  if "unsed_vars" in test["optimizations"]:
    ast, original_ast = test_unsed_vars(test["src"], ast)

  if benchmark:
    print_benchmark(test, original_ast, ast)

def test(tests: list[dict], print_results=False, output_file="tests/results.txt", benchmark=True):
  if not print_results:
    with open(output_file, "w"):
      pass
  for [index, test] in enumerate(tests, start=1):
      print (f"Testing source: {test['relative_path']}")
      if print_results:
          print_test(test, index, benchmark)
      if not print_results:
        with open(output_file, "a") as f:
            sys.stdout = f
            print_test(test, index, benchmark)
            sys.stdout = sys.__stdout__
  print (f"[bold][green]Tests completed![/green][/bold]")
  if not print_results:
    print (f"[bold]Run following command to view results:[/bold]")
    print (f"[blue]less -R {output_file}[/blue]")
