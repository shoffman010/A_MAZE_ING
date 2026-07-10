import sys

from config import load_config
from menu_ui import Menu


def main() -> int:
    """Load configuration and start the interactive maze application.

    Returns
    -------
    int
        Zero after a normal menu exit, or one when configuration loading,
        maze setup, or a user-requested file operation fails.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1

    try:
        config = load_config(sys.argv[1])

    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    menu = Menu()
    try:
        menu.run(config)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

