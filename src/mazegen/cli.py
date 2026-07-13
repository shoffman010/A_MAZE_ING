"""Provide command-line startup for the maze application.

This module validates the configuration argument, reports expected errors
without a traceback, and hands valid settings to the interactive menu.
"""

import sys
from collections.abc import Sequence

from .config import load_config
from .menu_ui import Menu


def main(argv: Sequence[str] | None = None) -> int:
    """Load configuration and start the interactive maze application.

    Args:
        argv: Command-line arguments without the executable name. When
            omitted, arguments are read from :data:`sys.argv`.

    Returns:
        Zero after a normal exit, or one when the arguments, configuration,
        or a requested file operation are invalid.
    """
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
