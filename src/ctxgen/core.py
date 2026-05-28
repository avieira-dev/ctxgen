"""
FILE: core.py
DESCRIPTION: File scanning, interactive selection, and output generation.
RESPONSIBILITIES:
  - Discover eligible files in a target directory
  - Present an interactive index-based file picker
  - Write selected files into a structured text bundle
"""

import sys
import time
from pathlib import Path
from ctxgen.utils.colors import Colors
from ctxgen.utils.messages import abort

_IGNORE_DIRS = {".git", "__pycache__", "venv", "env", "node_modules", ".idea", ".vscode", "dist", "build"}


def get_eligible_files(target_path: Path, extensions: list[str] | None, output_filename: str | None) -> list[Path]: 
    eligible = []

    for path in target_path.rglob("*"):
        rel_parts = path.parts[len(target_path.parts):]
        if any(p.startswith(".") or p in _IGNORE_DIRS for p in rel_parts):
            continue
        if not path.is_file():
            continue
        if extensions and path.suffix not in extensions:
            continue
        if output_filename and path.name == Path(output_filename).name:
            continue
        eligible.append(path)

    return sorted(eligible)


def prompt_file_selection(files: list[Path], target_path: Path) -> list[Path]:
    total = len(files)
    pad   = len(str(total))
    sep   = Colors.dim("─" * 90)

    print(f"  {Colors.cyan('▸')} {Colors.dim(str(total))} eligible file{'s' if total != 1 else ''} found in {Colors.dim(str(target_path))}")
    print()

    for idx, path in enumerate(files, 1):
        rel = path.relative_to(target_path)
        num = Colors.dim(f"[{str(idx).rjust(pad)}]")
        print(f"  {num}  {rel}")

    print()
    print(sep)
    print(f"  {Colors.dim('Selection syntax:')}")
    print(f"  {Colors.cyan('1,3,5')} {Colors.dim('specific files')}")
    print(f"  {Colors.cyan('1-4')} {Colors.dim('range')}")
    print(f"  {Colors.cyan('1-3,5,7')} {Colors.dim('mixed')}")
    print(f"  {Colors.cyan('all')} {Colors.dim('every file')}")
    print(f"  {Colors.cyan('q')} {Colors.dim('cancel')}")
    print(sep)
    print()

    while True:
        try:
            choice = input(f"  {Colors.dim('›')} Select files: ").strip().lower()
        except EOFError:
            abort()

        print()

        if choice == "q":
            abort()

        if choice == "all":
            return files

        selected_indices: set[int] = set()
        try:
            for part in choice.split(","):
                part = part.strip()
                if "-" in part:
                    start, end = part.split("-", 1)
                    selected_indices.update(range(int(start), int(end) + 1))
                else:
                    selected_indices.add(int(part))

            selected: list[Path] = []
            for idx in sorted(selected_indices):
                if 1 <= idx <= total:
                    selected.append(files[idx - 1])
                else:
                    print(f"  {Colors.yellow('!')} Index {idx} is out of range — skipping.")

            if not selected:
                print()
                print(f"  {Colors.error_abort('No valid files selected. Try again.')}\n")
                continue

            return selected

        except ValueError:
            print()
            print(f"  {Colors.error_abort('Invalid format. Use numbers, ranges (e.g. 1-5), or all.')}\n")

def _show_spinner(duration: float = 1.2) -> None:
    """Displays a modern terminal spinner for a short artificial duration."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for frame in frames:
            if time.time() >= end_time:
                break
            sys.stdout.write(f"\r  {Colors.cyan(frame)} Processing and bundling files...")
            sys.stdout.flush()
            time.sleep(0.08)
            
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()

def generate_output(selected_files: list[Path], target_path: Path, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    files_written = 0

    try:
        with output_file.open("w", encoding="utf-8") as out:
            for path in selected_files:
                if path.resolve() == output_file.resolve():
                    continue
                try:
                    content = path.read_text(encoding="utf-8")
                    rel = path.relative_to(target_path)

                    out.write(f"{'=' * 60}\n")
                    out.write(f"File: {rel}\n")
                    out.write(f"{'=' * 60}\n\n")
                    out.write(content)
                    out.write("\n\n")
                    files_written += 1

                except UnicodeDecodeError:
                    rel = path.relative_to(target_path)
                    print(f"  {Colors.yellow('!')} Skipped binary file: {Colors.dim(str(rel))}")

        _show_spinner(1.5)

    except OSError as e:
        _show_spinner(0.5)
        print(Colors.error_saving(str(output_file)))
        print(Colors.dim(f"  {e}"))
        sys.exit(1)

    print(Colors.dim("─" * 60))
    print()
    print(Colors.success(files_written, str(output_file)))
    print()