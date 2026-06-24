from maze import Maze
from position import Position


class MazeWriter:
    """Serialize generated mazes in the required text-file format."""

    def write_maze(
        self,
        maze: Maze,
        path: str,
        output_file: str,
    ) -> None:
        """Write the maze layout, markers, and solution route to a file.

        Parameters
        ----------
        maze : Maze
            Maze whose cells and markers will be serialized.
        path : list of Position
            Solved route from maze entry to exit.
        output_file : str
            Destination file path, overwritten if it already exists.
        """

        with open(output_file, "w") as file:

            for row in maze.grid:

                line = "".join(cell.hex_value for cell in row)

                file.write(line + "\n")
            file.write("\n")

            file.write(f"{maze.entry.col},{maze.entry.row}\n")

            file.write(f"{maze.exit.col},{maze.exit.row}\n")

            file.write(f"{self._path_to_directions(path)}\n")

    def _path_to_directions(
        self,
        path: list[Position],
    ) -> str:
        """Convert a route of adjacent positions into compass directions.

        Parameters
        ----------
        path : list of Position
            Ordered route of orthogonally adjacent maze cells.

        Returns
        -------
        str
            Compact sequence using ``N``, ``E``, ``S``, and ``W``.
        """

        directions: list[str] = []

        for current, next_position in zip(
            path,
            path[1:],
        ):

            row_difference = next_position.row - current.row

            col_difference = next_position.col - current.col

            if row_difference == -1:
                directions.append("N")

            elif row_difference == 1:
                directions.append("S")

            elif col_difference == 1:
                directions.append("E")

            elif col_difference == -1:
                directions.append("W")

        return "".join(directions)
