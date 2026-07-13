"""Command-line entry point for the maze application."""

import sys
from collections.abc import Sequence

from .config import load_config
from .menu_ui import Menu


def main(argv: Sequence[str] | None = None) -> int:
    """Load configuration and start the interactive maze application."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 1:
        print("Usage: maze-gen config.txt", file=sys.stderr)
        return 1

    try:
        config = load_config(arguments[0])
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    try:
        Menu().run(config)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0
