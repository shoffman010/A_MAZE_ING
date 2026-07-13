from .maze import Maze
from .position import Position


class Renderer:
    """Render a maze as coloured ANSI terminal art."""
    COLOR_CODES = {
        "BLACK": "90",
        "RED": "91",
        "GREEN": "92",
        "YELLOW": "93",
        "BLUE": "94",
        "MAGENTA": "95",
        "CYAN": "96",
        "WHITE": "97",
        "DEFAULT": "",
    }

    EMPTY = "  "

    ENTRY = "\033[92mEN\033[0m"
    EXIT = "\033[91mEX\033[0m"

    def __init__(
        self,
        wall_color: str = "DEFAULT",
        path_color: str = "RED",
        pattern_color: str = "CYAN",
    ) -> None:
        """Create a renderer with the requested display colours.

        Parameters
        ----------
        wall_color, path_color, pattern_color : str
            Valid colour names used to decorate walls, solution paths, and the
            protected pattern, respectively.
        """
        self.WALL = self._colorize("██", wall_color)
        # self.PATH = self._colorize("••", path_color)
        self.PATH = self._colorize("░░", path_color)
        self.PATTERN = self._colorize("██", pattern_color)

    def render(
        self,
        maze: Maze,
        path: list[Position] | None = None,
        current: Position | None = None,
    ) -> None:
        """Print a maze with its protected pattern, markers, and optional path.

        Parameters
        ----------
        maze : Maze
            Maze to render.
        path : list of Position or None, optional
            Solution route to overlay. When omitted, no route is drawn.
        """
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

    def _colorize(self, text: str, color: str) -> str:
        """Wrap text in an ANSI colour sequence when a colour is configured.

        Parameters
        ----------
        text : str
            Text to decorate.
        color : str
            Colour name present in :attr:`COLOR_CODES`.

        Returns
        -------
        str
            Original text for ``DEFAULT``; otherwise ANSI-coloured text.
        """
        color_code = self.COLOR_CODES[color]
        if not color_code:
            return text

        return f"\033[{color_code}m{text}\033[0m"

    def _draw_path(
        self,
        canvas: list[list[str]],
        path: list[Position],
    ) -> None:
        """Overlay a route on a visual maze canvas.

        Parameters
        ----------
        canvas : list of list of str
            Mutable terminal-art canvas.
        path : list of Position
            Ordered route whose cells and connecting passages are drawn.
        """

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

    def _create_wall_canvas(self, maze: Maze) -> list[list[str]]:
        """Create a wall-filled canvas sized for a maze.

        Parameters
        ----------
        maze : Maze
            Maze that determines the canvas dimensions.

        Returns
        -------
        list of list of str
            Canvas with two visual slots per maze cell plus an outer border.
        """
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
        """Clear canvas positions for open maze cells and passages.

        Parameters
        ----------
        canvas : list of list of str
            Wall-filled canvas to modify in place.
        maze : Maze
            Maze whose wall configuration is rendered.
        """
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
        """Place one marker in the canvas cell for a maze position.

        Parameters
        ----------
        canvas : list of list of str
            Canvas to modify in place.
        position : Position
            Maze cell where the marker is displayed.
        marker : str
            Rendered marker text.
        """
        # row, col = position
        canvas_row = position.row * 2 + 1
        canvas_col = position.col * 2 + 1
        canvas[canvas_row][canvas_col] = marker

    def _draw_42_pattern(
        self,
        canvas: list[list[str]],
        maze: Maze,
    ) -> None:
        """Draw the protected pattern over the maze canvas.

        Parameters
        ----------
        canvas : list of list of str
            Canvas to modify in place.
        maze : Maze
            Maze containing the cells marked as protected pattern cells.
        """
        for row_index, row in enumerate(maze.grid):
            for col_index, cell in enumerate(row):
                if not cell.pattern_42:
                    continue

                canvas_row = row_index * 2 + 1
                canvas_col = col_index * 2 + 1
                canvas[canvas_row][canvas_col] = self.PATTERN

                if (
                    row_index > 0
                    and maze.grid[row_index - 1][col_index].pattern_42
                ):
                    canvas[canvas_row - 1][canvas_col] = self.PATTERN

                if (
                    col_index > 0
                    and maze.grid[row_index][col_index - 1].pattern_42
                ):
                    canvas[canvas_row][canvas_col - 1] = self.PATTERN
