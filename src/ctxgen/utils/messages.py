"""
FILE: utils/messages.py
DESCRIPTION: Centralized terminal messaging, branding, and graceful shutdown utilities using Rich.
RESPONSIBILITIES:
  - Render modern, minimal header panels for CLI welcome screens (Purple Tech Theme)
  - Provide standardized terminal feedback messages and error panels
  - Handle graceful interruption and cancellation flows with consistent styling
"""

import signal
import sys
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def welcome_header() -> None:
    """Renders a clean, modern welcome panel with a Tech Purple palette."""
    header_text = Text()
    header_text.append("v2.0.0 ", style="bold black on magenta")
    header_text.append(" Turn entire projects into a single context for LLMs.", style="dim white")

    panel = Panel(
        header_text,
        title="[bold purple]Welcome to ctxgen![/bold purple]",
        border_style="magenta",
        box=box.ROUNDED,
        padding=(0, 2),
    )
    console.print()
    console.print(panel)
    console.print()

def abort(message: str | None = None) -> None:
    """Handles graceful termination with rich output formatting."""
    console.print()
    if message:
        console.print(f" [bold red]✗ Error:[/bold red] [dim]{message}[/dim]")
    
    console.print(" [bold yellow]⚠ Operation cancelled.[/bold yellow]")
    console.print(" [magenta]Bye![/magenta]\n")
    sys.exit(128 + signal.SIGINT)