from cell import Cell
from position import Position


class Maze:
    PATTERN_42: tuple[str, ...] = (
        "# # ###",
        "# #   #",
        "### ###",
        "  # #  ",
        "  # ###",
    )

    def __init__(
        self,
        rows: int,
        cols: int,
        entry: tuple[int, int] | None = None,
        exit: tuple[int, int] | None = None,
    ):
        self.rows = rows
        self.cols = cols

        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(cols)]
            for _ in range(rows)
        ]

        self._lock_42_pattern()
        self.entry = self._validated_marker(entry, (0, 0), "entry")
        self.exit = self._validated_marker(exit, (rows - 1, cols - 1), "exit")

        if self.entry == self.exit:
            raise ValueError("entry and exit must be different cells")

    def valid_cell(self, row: int, col: int) -> bool:
        return (
            0 <= row < self.rows
            and
            0 <= col < self.cols
        )

    def get_cell(self, row: int, col: int) -> Cell:
        return self.grid[row][col]

    def remove_wall(self,
                    current_row: int,
                    current_col: int,
                    next_row: int,
                    next_col: int) -> None:
        current = self.grid[current_row][current_col]
        neighbor = self.grid[next_row][next_col]

        if next_col == current_col - 1:
            neighbor.east = False
            current.west = False
        elif next_row == current_row - 1:
            neighbor.south = False
            current.north = False
        elif next_col == current_col + 1:
            neighbor.west = False
            current.east = False
        elif next_row == current_row + 1:
            current.south = False
            neighbor.north = False

    def get_neighbors(self, row: int, col: int) -> list[Position]:

        neighbors: list[Position] = []

        adjust_position = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]
        for adjust_row, adjust_col in adjust_position:
            new_row = row + adjust_row
            new_col = col + adjust_col
            if self.valid_cell(new_row, new_col):
                neighbors.append(Position(row=new_row, col=new_col))

        return neighbors

    def _lock_42_pattern(self) -> None:
        pattern_cells = self._scaled_42_pattern()

        pattern_height = len(pattern_cells)
        pattern_width = len(pattern_cells[0])
        start_row = (self.rows - pattern_height) // 2
        start_col = (self.cols - pattern_width) // 2

        for pattern_row, line in enumerate(pattern_cells):
            for pattern_col, mark in enumerate(line):
                if mark != "#":
                    continue

                row = start_row + pattern_row
                col = start_col + pattern_col
                self.grid[row][col].locked_42 = True

    def _scaled_42_pattern(self) -> tuple[str, ...]:
        base_height = len(self.PATTERN_42)
        base_width = max(len(row) for row in self.PATTERN_42)

        if self.rows < base_height or self.cols < base_width:
            raise ValueError(
                "maze is too small for the 42 pattern: "
                f"minimum size is {base_width}x{base_height}"
            )

        row_margin = 2 if self.rows > base_height + 2 else 0
        col_margin = 2 if self.cols > base_width + 2 else 0
        scale = min(
            max(1, (self.rows - row_margin) // base_height),
            max(1, (self.cols - col_margin) // base_width),
        )

        scaled_rows: list[str] = []
        for row in self.PATTERN_42:
            padded_row = row.ljust(base_width)
            scaled_row = "".join(mark * scale for mark in padded_row)
            scaled_rows.extend([scaled_row] * scale)

        return tuple(scaled_rows)

    def _validated_marker(
        self,
        position: tuple[int, int] | None,
        default: tuple[int, int],
        name: str,
    ) -> tuple[int, int]:
        row, col = position if position is not None else default

        if not self.valid_cell(row, col):
            raise ValueError(f"{name} must be inside the maze")

        if self.grid[row][col].locked_42:
            raise ValueError(f"{name} cannot be inside the 42 pattern")

        return row, col
