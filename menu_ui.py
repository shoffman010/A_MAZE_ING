from config import Config
from maze import Maze
from maze_solver import MazeSolver
from maze_generator import MazeGenerator
from maze_writer import MazeWriter
from position import Position
from renderer import Renderer
import time
import os


class Menu:
    """Provide the interactive terminal interface for maze operations."""
    COLORS = [
        "BLACK",
        "RED",
        "GREEN",
        "YELLOW",
        "BLUE",
        "MAGENTA",
        "CYAN",
        "WHITE",
        "DEFAULT",
    ]

    def _print_menu(self) -> None:
        print()
        print("=== A-Maze-ing ===")
        print("1. Generate new maze")
        print("2. Show solution")
        print("3. Hide solution")
        print("4. Change colors")
        print("5. Save maze")
        print("6. Exit")

    def _animate_solution(
        self,
        renderer: Renderer,
        maze: Maze,
        path: list[Position],
    ) -> None:

        for index in range(1, len(path) + 1):

            # print("\033[2J\033[H", end="")
            print("\033[H", end="")
            # os.system("cls" if os.name == "nt" else "clear")

            renderer.render(
                maze,
                path=path[:index],
            )

            time.sleep(0.05)

    def run(
        self,
        config: Config,
    ) -> None:
        """Run the maze generation and display menu until the user exits.

        Parameters
        ----------
        config : Config
            Validated settings used for initial generation and file output.
        """

        wall_color = config.wall_color
        path_color = config.path_color
        pattern_color = config.pattern_color

        maze = Maze(
            config.height,
            config.width,
            config.pattern,
            entry=Position(*config.entry),
            exit=Position(*config.exit),
        )

        generator = MazeGenerator(seed=config.seed)
        generator.generate(maze, perfect=config.perfect)

        show = False
        redraw_screen = True

        while True:

            renderer = Renderer(
                wall_color=wall_color,
                path_color=path_color,
                pattern_color=pattern_color,
            )

            if redraw_screen:
                # print("\033[2J\033[H", end="")
                os.system("cls" if os.name == "nt" else "clear")
                # print("\033[H", end="")

                if show:
                    solver = MazeSolver()
                    path = solver.solve(maze)

                    renderer.render(maze, path)
                else:
                    renderer.render(maze)

                self._print_menu()
            else:
                redraw_screen = True

            choice = input("Enter your choice :").strip()

            if choice == "1":
                maze = Maze(
                    config.height,
                    config.width,
                    config.pattern,
                    entry=Position(*config.entry),
                    exit=Position(*config.exit),
                )
                generator = MazeGenerator(seed=config.seed)
                generator.generate(maze, perfect=config.perfect)
                show = False
            elif choice == "2":
                solver = MazeSolver()
                path = solver.solve(maze)

                self._animate_solution(
                    renderer,
                    maze,
                    path,
                )
                show = True
                print("\033[J", end="")
                self._print_menu()
                redraw_screen = False
            elif choice == "3":
                show = False
            elif choice == "4":
                wall_color = self._choose_color(
                    "Wall",
                    wall_color,
                )
                path_color = self._choose_color(
                    "Path",
                    path_color,
                )
                pattern_color = self._choose_color(
                    "Pattern",
                    pattern_color,
                )
            elif choice == "5":
                solver = MazeSolver()
                path = solver.solve(maze)
                writer = MazeWriter()
                writer.write_maze(
                    maze,
                    path,
                    config.output_file,
                )
                print()
                print(f"Saved to {config.output_file}")
                input("Press Enter to continue...")
            elif choice == "6":
                break
            else:
                input("Please enter valid number from 1-6. Press Enter to continue...")

    def _choose_color(
        self,
        name: str,
        current: str,
    ) -> str:
        """Prompt until the user selects a supported display colour.

        Parameters
        ----------
        name : str
            Human-readable label for the colour being changed.
        current : str
            Currently selected colour name.

        Returns
        -------
        str
            Newly selected colour name from :attr:`COLORS`.
        """

        while True:

            print()
            print(f"{name} color " f"(current: {current})")

            for index, color in enumerate(
                self.COLORS,
                start=1,
            ):
                print(f"{index}. {color}")

            choice = input("Enter color choice: ").strip()

            try:
                choice_number = int(choice)

                if 1 <= choice_number <= len(self.COLORS):
                    return self.COLORS[choice_number - 1]

            except ValueError:
                pass

            print()
            print(f"Please enter a number " f"between 1 and {len(self.COLORS)}.")
