"""
FILE: cli.py
DESCRIPTION: Argument parsing and command dispatch using Rich for help display.
RESPONSIBILITIES:
  - Define the CLI surface (subcommands, flags, defaults)
  - Validate inputs and resolve paths
  - Delegate to core functions
"""

import argparse
import sys
from pathlib import Path
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from ctxgen.core import generate_output, get_eligible_files, prompt_file_selection
from ctxgen.utils.messages import abort

console = Console()

class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        console.print(f"[bold red]ctxgen error:[/bold red] {message}\n")
        sys.exit(2)

def _print_help() -> None:
    help_content = Text()

    # Usage
    help_content.append("Usage:\n", style="bold magenta")
    help_content.append("  ctxgen <group> <command> [options]\n\n", style="dim white")

    # Commands
    help_content.append("Groups & Commands:\n", style="bold magenta")
    help_content.append("  ▸ ", style="bold white")
    help_content.append("generate txt", style="bold purple")
    help_content.append("    Bundle source files into a single .txt context\n\n", style="dim white")

    # Options
    help_content.append("Options (generate txt):\n", style="bold magenta")
    help_content.append("  ▸ ", style="bold white")
    help_content.append("-d, --dir  DIR", style="bold violet")
    help_content.append("     Source directory to scan ", style="default")
    help_content.append("(default: .)\n", style="dim")
    
    help_content.append("  ▸ ", style="bold white")
    help_content.append("-o, --out  FILE", style="bold violet")
    help_content.append("    Output file ", style="default")
    help_content.append("(default: <dir-name>.txt in CWD)\n", style="dim")
    
    help_content.append("  ▸ ", style="bold white")
    help_content.append("-e, --ext  EXT+", style="bold violet")
    help_content.append("    Filter by extensions ", style="default")
    help_content.append("(e.g. -e .py .cpp)\n", style="dim")
    
    help_content.append("  ▸ ", style="bold white")
    help_content.append("-h, --help", style="bold violet")
    help_content.append("        Show this help message and exit\n\n", style="default")

    # Examples
    help_content.append("Examples:\n", style="bold magenta")
    help_content.append("  $ ctxgen generate txt\n", style="purple")
    help_content.append("  $ ctxgen generate txt -d ~/Projects/my-app -e .py .h\n", style="purple")
    help_content.append("  $ ctxgen generate txt -o ./context.txt\n\n", style="purple")

    # Author / Footer
    help_content.append("Created by ", style="dim white")
    help_content.append("Alexandre Vieira", style="dim bold")
    help_content.append(" (https://github.com/avieira-dev)\n", style="bold purple")

    panel = Panel(
        help_content,
        title="[bold purple]ctxgen CLI Help[/bold purple]",
        border_style="magenta",
        box=box.ROUNDED,
        padding=(1, 2),
    )

    console.print()
    console.print(panel)
    console.print()
    sys.exit(0)

def _build_parser() -> argparse.ArgumentParser:
    parser = Parser(prog="ctxgen", add_help=False)

    top = parser.add_subparsers(dest="group")
    generate = top.add_parser("generate", add_help=False)

    sub = generate.add_subparsers(dest="command")
    txt = sub.add_parser("txt", add_help=False)
    txt.add_argument("-d", "--dir",  default=".",  metavar="DIR")
    txt.add_argument("-o", "--out",  default=None, metavar="FILE")
    txt.add_argument("-e", "--ext",  nargs="+",    metavar="EXT")

    return parser

def run() -> None:
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        _print_help()

    parser = _build_parser()
    args   = parser.parse_args()

    if args.group == "generate" and args.command == "txt":
        target = Path(args.dir).resolve()
        if not target.is_dir():
            abort(f"Directory '{args.dir}' does not exist.")

        output = (
            Path(args.out).expanduser().resolve()
            if args.out
            else Path.cwd() / f"{target.name}.txt"
        )

        files = get_eligible_files(target, args.ext, output.name)
        if not files:
            abort("No matching files found in the directory.")

        selected = prompt_file_selection(files, target)
        generate_output(selected, target, output)