"""Provide the module-based entry point for A-Maze-ing.

Running ``python -m mazegen`` delegates to the same command-line function as
the installed ``maze-gen`` command.
"""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
