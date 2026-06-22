import sys

from config import load_config
from maze import Maze
from renderer import Renderer
from position import Position
from maze_generator import MazeGenerator
from maze_writer import MazeWriter
from maze_solver import MazeSolver


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
            config.pattern,
            entry=Position(*config.entry),
            exit=Position(*config.exit),
        )
        # print(config)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    generator = MazeGenerator(seed=config.seed)
    generator.generate(maze, perfect=config.perfect)
    
    renderer = Renderer(
        wall_color=config.wall_color,
        path_color=config.path_color,
        pattern_color=config.pattern_color,
    )
    # renderer.render(maze)

    solver = MazeSolver()
    path = solver.solve(maze)
    writer = MazeWriter()

    writer.write_maze(
    maze,
    path,
    config.output_file,)
    renderer.render(maze, path,)


    return 0


if __name__ == "__main__":
    raise SystemExit(main())





# stty size -- to check bash... col row for terminals
