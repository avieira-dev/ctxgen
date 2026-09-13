"""
FILE: main.py
DESCRIPTION: Entry-point. Wires together welcome header and CLI dispatch.
"""

from ctxgen.cli import run
from ctxgen.utils.messages import abort, welcome_header

def main() -> None:
    welcome_header()

    try:
        run()
    except KeyboardInterrupt:
        abort()

if __name__ == "__main__":
    main()