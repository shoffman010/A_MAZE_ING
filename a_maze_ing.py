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
        # maze = Maze(
        #     config.height,
        #     config.width,
        #     config.pattern,
        #     entry=Position(*config.entry),
        #     exit=Position(*config.exit),
        # )
        # print(config)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # generator = MazeGenerator(seed=config.seed)
    # generator.generate(maze, perfect=config.perfect)

    # renderer = Renderer(
    #     wall_color=config.wall_color,
    #     path_color=config.path_color,
    #     pattern_color=config.pattern_color,
    # )
    # # renderer.render(maze)

    # solver = MazeSolver()
    # path = solver.solve(maze)
    # writer = MazeWriter()

    # writer.write_maze(
    # maze,
    # path,
    # config.output_file,)
    # renderer.render(maze, path,)

    menu = Menu()
    try:
        menu.run(config)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# stty size -- to check bash... col row for terminals
