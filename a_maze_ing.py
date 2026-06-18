import sys

from config import load_config
from maze import Maze
from renderer import Renderer


def main() -> int:
    """Load the config file, create the maze, and render it."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1

    try:
        config = load_config(sys.argv[1])
        maze = Maze(
            config.height,
            config.width,
            entry=config.entry,
            exit=config.exit,
        )
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    renderer = Renderer()
    renderer.render(maze)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
