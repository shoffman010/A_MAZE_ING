import sys

from config import load_config
from maze import Maze
from renderer import Renderer
from position import Position
from maze_generator import MazeGenerator


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
            entry=Position(*config.entry),
            exit=Position(*config.exit),
        )
        print(config)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    generator = MazeGenerator()
    generator.generate(maze)

    renderer = Renderer()
    renderer.render(maze)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
