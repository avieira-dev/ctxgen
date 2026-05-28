"""
FILE: cli.py
DESCRIPTION: Argument parsing and command dispatch.
RESPONSIBILITIES:
  - Define the CLI surface (subcommands, flags, defaults)
  - Validate inputs and resolve paths
  - Delegate to core functions
"""

import sys
import argparse
from pathlib import Path
from ctxgen.utils.colors import Colors
from ctxgen.utils.messages import abort
from ctxgen.core import get_eligible_files, prompt_file_selection, generate_output

_SEP = Colors.dim("─" * 90)

class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"ctxgen: error: {message}")
        print()
        sys.exit(2)

def _print_help() -> None:
    print("\n".join([
        "",
        f" {Colors.BOLD}HELP{Colors.END}",
        _SEP,
        "",
        f"  {Colors.dim('Usage:')}  ctxgen <group> <command> [options]",
        "",
        f"  {Colors.cyan('Groups & Commands')}",
        f"  {Colors.WHITE}▸{Colors.END} {Colors.BOLD}generate txt{Colors.END} >> Bundle source files into a .txt context",
        "",
        f"  {Colors.cyan('Options  (generate txt)')}",
        f"  {Colors.WHITE}▸{Colors.END} {Colors.BOLD}-d, --dir{Colors.END} >> DIR Source directory to scan  {Colors.dim('(default: .)')}",
        f"  {Colors.WHITE}▸{Colors.END} {Colors.BOLD}-o, --out{Colors.END} >> FILE Output file  {Colors.dim('(default: <dir-name>.txt in CWD)')}",
        f"  {Colors.WHITE}▸{Colors.END} {Colors.BOLD}-e, --ext{Colors.END} >> EXT+ Filter extensions  {Colors.dim('(e.g. -e .py .cpp)')}",
        f"  {Colors.WHITE}▸{Colors.END} {Colors.BOLD}-h, --help{Colors.END} >> Show this message and exit",
        "",
        f"  {Colors.cyan('Examples')}",
        f"  {Colors.WHITE}▸{Colors.END} {Colors.dim('ctxgen generate txt')}",
        f"  {Colors.WHITE}▸{Colors.END} {Colors.dim('ctxgen generate txt -d ~/Projects/ptah-engine -e .cpp .h')}",
        f"  {Colors.WHITE}▸{Colors.END} {Colors.dim('ctxgen generate txt -o ./context.txt')}",
        "",
        _SEP,
        "",
    ]))
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