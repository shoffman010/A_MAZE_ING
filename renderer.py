from maze import Maze
# class Renderer:
#     OUT_TOP_LEFT = "╔"
#     OUT_TOP_RIGHT = "╗"
#     OUT_BOTTOM_LEFT = "╚"
#     OUT_BOTTOM_RIGHT = "╝"
#     OUT_VERTICAL = "║"
#     OUT_HORIZONTAL = "═"

#     IN_VERTICAL = "│"
#     IN_HORIZONTAL = "─"
    
#     # def render(self, maze: Maze) -> None:
#     #     for row in maze.grid:
#     #         for _ in row:
                
        
        
#         print()
#         print("==================Hex Value =================")
#         for row in maze.grid:
#             line = "".join(cell.hex_value for cell in row)
#             print(line)


class Renderer:
    WALL = "██"
    EMPTY = "  "

    ENTRY = "EE"
    EXIT = "XX"
    PATH = ".."
    PATTERN = "42"

    def render(self, maze: Maze) -> None:
        """Print a block-style terminal representation of the maze."""
        canvas = self._create_wall_canvas(maze)

        self._carve_maze(canvas, maze)

        # Optional, only if these attributes exist on your Maze.
        if hasattr(maze, "entry"):
            self._draw_cell_marker(canvas, maze.entry, self.ENTRY)

        if hasattr(maze, "exit"):
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
                if getattr(cell, "is_pattern", False):
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