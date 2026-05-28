"""
FILE: main.py
DESCRIPTION: Entry-point. Wires together banner, version, and CLI dispatch.
"""

from ctxgen.utils.messages import banner, version, abort
from ctxgen.cli import run

def main() -> None:
    banner()
    version()

    try:
        run()
    except KeyboardInterrupt:
        print()
        abort()


if __name__ == "__main__":
    main()