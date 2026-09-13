"""
FILE: core.py
DESCRIPTION: File scanning, interactive selection, and output generation with real-time progress.
RESPONSIBILITIES:
  - Discover eligible files in a target directory
  - Present a directory tree view and interactive checkbox file picker (Tech Purple styled)
  - Write selected files into a structured text bundle and report rich stats
"""

import sys
from pathlib import Path
from InquirerPy.base.control import Choice
from InquirerPy.prompts.checkbox import CheckboxPrompt
from InquirerPy.utils import get_style
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table
from rich.tree import Tree
from ctxgen.utils.messages import abort

console = Console()

_IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    "env",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
}

PURPLE_STYLE = get_style(
    {
        "questionmark": "magenta bold",
        "pointer": "magenta bold",
        "checkbox": "purple bold",
        "answertoken": "white bold",
        "instruction": "#888888",
        "question": "white bold",
    },
    style_override=True,
)

def get_eligible_files(target_path: Path, extensions: list[str] | None, output_filename: str | None) -> list[Path]:
    eligible = []

    for path in target_path.rglob("*"):
        rel_parts = path.parts[len(target_path.parts) :]
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

def _build_file_tree(files: list[Path], target_path: Path) -> Tree:
    """Generates a Rich Tree representation of eligible files relative to target_path."""
    root_node = Tree(
        f"[bold magenta]📁 {target_path.name}/[/bold magenta]",
        guide_style="magenta",
    )
    nodes = {Path("."): root_node}

    for file_path in files:
        rel_path = file_path.relative_to(target_path)
        current_node = root_node
        
        for parent in list(reversed(rel_path.parents))[:-1]:
            if parent not in nodes:
                nodes[parent] = current_node.add(
                    f"[bold purple]📁 {parent.name}/[/bold purple]"
                )
            current_node = nodes[parent]

        current_node.add(f"[dim white]📄 {rel_path.name}[/dim white]")

    return root_node

def prompt_file_selection(files: list[Path], target_path: Path) -> list[Path]:
    total = len(files)

    console.print(
        f" [bold magenta]▸[/bold magenta] [bold white]{total}[/bold white] "
        f"[dim white]eligible file{'s' if total != 1 else ''} found in[/dim white] "
        f"[magenta]{target_path}[/magenta]\n"
    )

    tree = _build_file_tree(files, target_path)
    console.print(tree)
    console.print()

    choices = [
        Choice(value=path, name=str(path.relative_to(target_path)), enabled=True)
        for path in files
    ]

    console.print("[dim white]Select files to include in context:[/dim white]")

    try:
        selected = CheckboxPrompt(
            message="",
            qmark="",
            amark="",
            choices=choices,
            style=PURPLE_STYLE,
            long_instruction="(Space: toggle, Ctrl+A: toggle all, Enter: confirm)",
            pointer="❯",
            enabled_symbol="✔ ",
            disabled_symbol="✘ ",
            show_cursor=False,
        ).execute()
    except KeyboardInterrupt:
        abort()

    if not selected:
        abort("No files were selected.")

    return selected

def _format_size(size_bytes: int) -> str:
    """Formats raw byte counts into human-readable KB or MB strings."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def generate_output(selected_files: list[Path], target_path: Path, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    files_written = 0
    total_lines = 0

    progress_bar = Progress(
        SpinnerColumn(spinner_name="dots", style="bold magenta"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, complete_style="magenta", finished_style="purple"),
        TaskProgressColumn(style="dim white"),
        console=console,
        transient=True,
    )

    try:
        with progress_bar:
            task = progress_bar.add_task(
                "Bundling files...", total=len(selected_files)
            )

            with output_file.open("w", encoding="utf-8") as out:
                for path in selected_files:
                    if path.resolve() == output_file.resolve():
                        progress_bar.advance(task)
                        continue
                    try:
                        content = path.read_text(encoding="utf-8")
                        rel = path.relative_to(target_path)

                        header = f"{'=' * 60}\nFile: {rel}\n{'=' * 60}\n\n"
                        out.write(header)
                        out.write(content)
                        out.write("\n\n")

                        files_written += 1
                        total_lines += content.count("\n") + 1
                    except UnicodeDecodeError:
                        rel = path.relative_to(target_path)
                        console.print(
                            f"  [bold yellow]![/bold yellow] Skipped binary file: [dim]{rel}[/dim]"
                        )

                    progress_bar.advance(task)

    except OSError as e:
        console.print(f" [bold red]✗ Error saving file:[/bold red] {output_file}")
        console.print(f"  [dim]{e}[/dim]")
        sys.exit(1)

    file_size = output_file.stat().st_size
    formatted_size = _format_size(file_size)

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold magenta")
    table.add_column(style="white")

    table.add_row(
        "Status:", "[bold purple]✔ Context Generated Successfully[/bold purple]"
    )
    table.add_row("Output File:", f"[dim white]{output_file}[/dim white]")
    table.add_row(
        "Files Bundled:", f"[bold magenta]{files_written}[/bold magenta] files"
    )
    table.add_row("Total Lines:", f"[bold magenta]{total_lines:,}[/bold magenta] lines")
    table.add_row("File Size:", f"[bold purple]{formatted_size}[/bold purple]")

    stats_panel = Panel(
        table,
        title="[bold purple] Summary Metrics [/bold purple]",
        border_style="magenta",
        box=box.ROUNDED,
        padding=(1, 2),
    )

    console.print()
    console.print(stats_panel)
    console.print()