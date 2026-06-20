from maze import Maze
from position import Position

class Renderer:
    WALL = "██"
    # WALL = "\033[30m██\033[0m"
    EMPTY = "  "
    # EMPTY   = "\033[31m  \033[0m"

    ENTRY = "\033[92mEN\033[0m"
    EXIT = "\033[91mEX\033[0m"
    PATH = "\033[91m..\033[0m"
    PATTERN = "\033[96m██\033[0m"



    # WALL = "█"
    # # WALL = "\033[30m██\033[0m"
    # EMPTY = " "
    # # EMPTY   = "\033[31m  \033[0m"

    # ENTRY = "\033[92mN\033[0m"
    # EXIT = "\033[91mX\033[0m"
    # PATH = "\033[91m.\033[0m"
    # PATTERN = "\033[96m█\033[0m"


    def _draw_path(
    self,
    canvas: list[list[str]],
    path: list[Position],) -> None:

        for index, position in enumerate(path):

            canvas_row = position.row * 2 + 1
            canvas_col = position.col * 2 + 1

            canvas[canvas_row][canvas_col] = self.PATH

            if index == 0:
                continue

            previous = path[index - 1]

            previous_row = previous.row * 2 + 1
            previous_col = previous.col * 2 + 1

            wall_row = (canvas_row + previous_row) // 2
            wall_col = (canvas_col + previous_col) // 2

            canvas[wall_row][wall_col] = self.PATH


    def render(self, maze: Maze, path: list[Position] | None = None,) -> None:
        """Print a block-style terminal representation of the maze."""
        canvas = self._create_wall_canvas(maze)

        self._carve_maze(canvas, maze)
        
        if path is not None:
            self._draw_path(
                canvas,
                path,
            )
        self._draw_42_pattern(canvas, maze)
        self._draw_cell_marker(canvas, maze.entry, self.ENTRY)
        self._draw_cell_marker(canvas, maze.exit, self.EXIT)

        for row in canvas:
            print("".join(row))

    def _create_wall_canvas(self, maze: Maze) -> list[list[str]]:
        visual_rows = maze.rows * 2 + 1
        visual_cols = maze.cols * 2 + 1

        return [
            [self.WALL for _ in range(visual_cols)]
            for _ in range(visual_rows)
        ]

    def _carve_maze(
        self,
        canvas: list[list[str]],
        maze: Maze,
    ) -> None:
        for row_index, row in enumerate(maze.grid):
            for col_index, cell in enumerate(row):
                canvas_row = row_index * 2 + 1
                canvas_col = col_index * 2 + 1

                if cell.locked_42:
                    continue

                canvas[canvas_row][canvas_col] = self.EMPTY

                if not cell.north:
                    canvas[canvas_row - 1][canvas_col] = self.EMPTY

                if not cell.east:
                    canvas[canvas_row][canvas_col + 1] = self.EMPTY

                if not cell.south:
                    canvas[canvas_row + 1][canvas_col] = self.EMPTY

                if not cell.west:
                    canvas[canvas_row][canvas_col - 1] = self.EMPTY

    def _draw_cell_marker(
        self,
        canvas: list[list[str]],
        position: Position,
        marker: str,
    ) -> None:
        # row, col = position
        canvas_row = position.row * 2 + 1
        canvas_col = position.col * 2 + 1
        canvas[canvas_row][canvas_col] = marker

    def _draw_42_pattern(
        self,
        canvas: list[list[str]],
        maze: Maze,
    ) -> None:
        for row_index, row in enumerate(maze.grid):
            for col_index, cell in enumerate(row):
                if not cell.locked_42:
                    continue

                canvas_row = row_index * 2 + 1
                canvas_col = col_index * 2 + 1
                canvas[canvas_row][canvas_col] = self.PATTERN

                if row_index > 0 and\
                        maze.grid[row_index - 1][col_index].locked_42:
                    canvas[canvas_row - 1][canvas_col] = self.PATTERN

                if col_index > 0 and\
                        maze.grid[row_index][col_index - 1].locked_42:
                    canvas[canvas_row][canvas_col - 1] = self.PATTERN
