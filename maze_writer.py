from maze import Maze

class MazeWriter:

    def write_maze(self, maze: Maze, path: str, ) -> None:

        with open(path, "w") as file:

            for row in maze.grid:

                line = "".join(
                    cell.hex_value
                    for cell in row
                )

                file.write(line + "\n")