from pathlib import Path
from lox import ast, Ctx
import time
import shutil
import re
from rich import print

BASE_DIR = Path(__file__).parent.parent
EXAMPLES = BASE_DIR / "exemplos" / "optimization"

LEX_REGEX = re.compile(
  r"""
  (?://\ *optimizations:\ (?P<OPTIMIZATIONS>[^\n]*))
  | (?://[^\n]*description:\ (?P<DESCRIPTION>[^\n]*))
  | (?P<COMMENT>//[^\n])
  | (?P<IGNORE>[^"/]+|"[^"]*"|//[^\n]*)
  """,
  re.VERBOSE
)


def parse_file_metadata(file_content: str, file_path: Path) -> dict[str, any]:
  optimizations = []
  description = ""
  for m in LEX_REGEX.finditer(file_content):
    if m.lastgroup == "OPTIMIZATIONS":
      optimizations = m.group("OPTIMIZATIONS").strip().split(",")
    elif m.lastgroup == "DESCRIPTION":
      description = m.group("DESCRIPTION").strip()
    elif m.lastgroup in ("COMMENT", "IGNORE"):
      continue
  
  return {
    "src": file_content,
    "file": file_path.name,
    "path": str(file_path.resolve()),
    "relative_path": str(file_path.relative_to(BASE_DIR)),
    "optimizations": optimizations,
    "description": description,
  }

def load_examples(
    folder: Path = EXAMPLES,
) -> list[dict[str, any]]:
    examples = []
    folders_of_examples = list(folder.iterdir())

    for file_path in folders_of_examples:
        if file_path.is_dir():
            folders_of_examples += list(file_path.iterdir())
            continue
        if not file_path.suffix == ".lox":
            continue

        try:
          with open(file_path, "r", encoding="utf-8") as file:
              src = file.read()
              metadata = parse_file_metadata(src, file_path)
              examples.append(metadata)

        except FileNotFoundError:
          print(f"[red]File not found: {file_path}[/red]")
          exit(1)

    examples.sort(key=lambda x: x["file"])
    return examples
  
  
def test_benchmark(ast: ast.Program):
  """
  Roda os testes de benchmark para o AST fornecido.
  """
  starttime = time.time()
  ctx = Ctx()
  ast.eval(ctx)
  endtime = time.time()
  return {
    "execution_time": endtime - starttime,
    "variables": ctx.scope,
  }
  
def printCode(src: str):
  prints = []
  lines = src.splitlines()[3:] # 3 to ignore header
  width = shutil.get_terminal_size().columns

  max_length = max(len(line) for line in lines)
  
  if max_length > width:
    print(f"[red]Warning: Source code line length exceeds terminal width ({width} characters).[/red]")
    max_length = width
    
  linenoSize = len(str(len(lines)))
  max_length_with_lines_no = max(max_length, linenoSize + 4) + 5
  
  prints.append("┌" + "─" * max_length_with_lines_no + "┐")
  
  prints.append(f"│ {'Source Code':^{max_length_with_lines_no -2}} │")
  
  prints.append("├" + "─" * max_length_with_lines_no + "┤")

  for line in lines:
    line = line.rstrip()
    if len(line) > max_length:
      line = line[:max_length - 3] + "..."
    lineno = lines.index(line) + 1
    prints.append(f"│ {lineno:>2} {line:<{max_length}} │")
  prints.append("└" + "─" * max_length_with_lines_no + "┘")
  
  return "\n".join(prints) 

def pretty_test(code: dict, identifier: str) -> str:
    toPrint = [
      f"\n\n[bold]Test {identifier}[/bold]"
      f"\n[italic]File:[/italic] [green]{code['relative_path']}[/green]"
      f"\n[bold]Optimizations:[/bold] [italic][green]{', '.join(code['optimizations'])}[/green][/italic]",
      "\n",
      printCode(code["src"]),
    ]

    return "".join(toPrint)

def print_benchmark(test: dict, original_ast: ast.Program, ast: ast.Program):
  description = str(test["description"]).split("\\n")
  print("[bold][green]Description:[/green][/bold]")
  for line in description:
    print(f"[green][italic]{line.strip()}[/italic][/green]")
  print("\n")
  print("[bold][italic]Running BENCHMARKS to src code[/italic][/bold]")
  original_bench = test_benchmark(original_ast)
  optimized_bench = test_benchmark(ast)
  print(f"\n[bold][red]Original AST Execution Time: {original_bench['execution_time']} seconds[/red][/bold]")
  print(f"[bold][magenta]Optimized AST Execution Time: {optimized_bench['execution_time']} seconds[/magenta][/bold]")
  print(f"[bold][blue]Variables in original AST: {original_bench['variables']}[/blue][/bold]")
  print(f"[bold][yellow]Variables in optimized AST: {optimized_bench['variables']}[/yellow][/bold]")
  times_faster = original_bench["execution_time"] // (optimized_bench["execution_time"] if optimized_bench["execution_time"] != 0 else 1)
  print(f"[italic]Optimized it was {times_faster}x faster than original[/italic]")
  print("\n[bold][green]BENCHMARKS completed![/green][/bold]\n")