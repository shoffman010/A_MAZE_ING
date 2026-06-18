from maze import Maze


class Renderer:
    WALL = "██"
    EMPTY = "  "

    ENTRY = "\033[92mEN\033[0m"
    EXIT = "\033[91mEX\033[0m"
    PATH = "\033[93m..\033[0m"
    PATTERN = "\033[96m██\033[0m"

    def render(self, maze: Maze) -> None:
        """Print a block-style terminal representation of the maze."""
        canvas = self._create_wall_canvas(maze)

        self._carve_maze(canvas, maze)
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

                # If this cell belongs to your closed 42 pattern,
                # do not carve it open.
                if cell.locked_42:
                    continue

                # Carve the cell center.
                canvas[canvas_row][canvas_col] = self.EMPTY

                # Carve passages only when the wall is open.
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
        position: tuple[int, int],
        marker: str,
    ) -> None:
        row, col = position
        canvas_row = row * 2 + 1
        canvas_col = col * 2 + 1
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

                if row_index > 0 and maze.grid[row_index - 1][col_index].locked_42:
                    canvas[canvas_row - 1][canvas_col] = self.PATTERN

                if col_index > 0 and maze.grid[row_index][col_index - 1].locked_42:
                    canvas[canvas_row][canvas_col - 1] = self.PATTERN
