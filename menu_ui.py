from config import Config
from maze import Maze
from maze_solver import MazeSolver
from maze_generator import MazeGenerator
from maze_writer import MazeWriter
from position import Position
from renderer import Renderer

class Menu:
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

    def run(
        self,
        config: Config,
    ) -> None:

        wall_color=config.wall_color
        path_color=config.path_color
        pattern_color=config.pattern_color

        maze = Maze(
            config.height,
            config.width,
            config.pattern,
            entry=Position(*config.entry),
            exit=Position(*config.exit),
        )

        generator = MazeGenerator(seed=config.seed)
        generator.generate(maze, perfect=config.perfect)
        
        # renderer.render(maze)

        show = False

        while True:

            renderer = Renderer(
            wall_color=wall_color,
            path_color=path_color,
            pattern_color=pattern_color,)

            print("\033[2J\033[H", end="")

            if show:
                solver = MazeSolver()
                path = solver.solve(maze)
                renderer.render(maze, path)
            else:
                renderer.render(maze)

            print()
            print("=== A-Maze-ing ===")
            print("1. Generate new maze")
            print("2. Show solution")
            print("3. Hide solution")
            print("4. Change colors")
            print("5. Save maze")
            print("6. Exit")

            choice = input("Enter your choice :").strip()

            if choice == '1':
                maze = Maze(
                    config.height,
                    config.width,
                    config.pattern,
                    entry=Position(*config.entry),
                    exit=Position(*config.exit),
                )
                generator.generate(maze, perfect=config.perfect)
                show = False
            elif choice == '2':
                show = True
            elif choice == '3':
                show = False
            elif choice == '4':
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
            elif choice == '5':
                solver = MazeSolver()
                path = solver.solve(maze)
                writer = MazeWriter()
                writer.write_maze(
                    maze, path, config.output_file,)
                print()
                print(
                    f"Saved to {config.output_file}"
                )
                input("Press Enter to continue...")
            elif choice == '6':
                break
            else:
                input("Please enter valid number from 1-6. Press Enter to continue...")
            

    def _choose_color(
    self,
    name: str,
    current: str,
) -> str:

        while True:

            print()
            print(
                f"{name} color "
                f"(current: {current})"
            )

            for index, color in enumerate(
                self.COLORS,
                start=1,
            ):
                print(
                    f"{index}. {color}"
                )

            choice = input("Enter color choice: ").strip()

            try:
                choice_number = int(choice)

                if 1 <= choice_number <= len(self.COLORS):
                    return self.COLORS[
                        choice_number - 1
                    ]

            except ValueError:
                pass

            print()
            print(
                f"Please enter a number "
                f"between 1 and {len(self.COLORS)}."
            )