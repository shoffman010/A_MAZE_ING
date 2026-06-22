from cell import Cell
from position import Position
from direction import Direction

class Maze:
    """A grid maze with an untouchable, locked pattern."""

    PATTERNS = {"42": (
        "# # ###",
        "# #   #",
        "### ###",
        "  # #  ",
        "  # ###",
    ),
    "X": (
        "#   #",
        " # # ",
        "  #  ",
        " # # ",
        "#   #",
    ),
    "Box":
        (
            "######",
            "#    # ",
            "#    # ",
            "#    # ",            
            "######",
        )
    
    }

    def __init__(
        self,
        rows: int,
        cols: int,
        pattern_name: str,
        entry: Position | None = None,
        exit: Position | None = None,
    ):
        self.rows = rows
        self.cols = cols

        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(cols)]
            for _ in range(rows)
        ]
        if pattern_name not in self.PATTERNS:
            valid_patterns = ", ".join(
                self.PATTERNS.keys()
            )

            raise ValueError(
                f"unknown pattern '{pattern_name}'. "
                f"Valid patterns: {valid_patterns}"
            )

        self.pattern = self.PATTERNS[pattern_name]

        self._lock_42_pattern()
        self.entry = self._validated_marker(entry, Position(0, 0), "entry")
        self.exit = self._validated_marker(exit, Position(rows - 1, cols - 1), "exit")

        if self.entry == self.exit:
            raise ValueError("entry and exit must be different cells")

    def valid_cell(self, position: Position) -> bool:
        return (
            0 <= position.row < self.rows
            and
            0 <= position.col < self.cols
        )

    def get_cell(self, position: Position) -> Cell:
        return self.grid[position.row][position.col]

    def remove_wall(self,
                    current: Position,
                    neighbor: Position) -> None:
        """Open the shared wall between two adjacent cells."""
        current_cell = self.grid[current.row][current.col]
        neighbor_cell = self.grid[neighbor.row][neighbor.col]

        if neighbor.col == current.col - 1:
            neighbor_cell.east = False
            current_cell.west = False

        elif neighbor.row == current.row - 1:
            neighbor_cell.south = False
            current_cell.north = False

        elif neighbor.col == current.col + 1:
            neighbor_cell.west = False
            current_cell.east = False

        elif neighbor.row == current.row + 1:
            current_cell.south = False
            neighbor_cell.north = False

    def get_neighbors(self, position: Position) -> list[Position]:
        """Return adjacent cells that are not part of the locked pattern."""

        neighbors: list[Position] = []

        # adjust_position = [
        #     (-1, 0),
        #     (1, 0),
        #     (0, -1),
        #     (0, 1)
        # ]
        for direction in Direction:
            new_neighbor = position.move(direction)
            if self.valid_cell(new_neighbor) and not self.get_cell(new_neighbor).locked_42:
                neighbors.append(new_neighbor)

        return neighbors
    
    def get_reachable_neighbors(
    self,
    position: Position,) -> list[Position]:
        """Return adjacent unlocked cells connected by an open wall."""
        neighbors: list[Position] = []

        cell = self.get_cell(position)

        if not cell.north:

            neighbor = Position(
                position.row - 1,
                position.col,
            )

            if self.valid_cell(neighbor) and not self.get_cell(neighbor).locked_42:
                neighbors.append(neighbor)

        if not cell.east:

            neighbor = Position(
                position.row,
                position.col + 1,
            )

            if self.valid_cell(neighbor) and not self.get_cell(neighbor).locked_42:
                neighbors.append(neighbor)

        if not cell.south:

            neighbor = Position(
                position.row + 1,
                position.col,
            )

            if self.valid_cell(neighbor) and not self.get_cell(neighbor).locked_42:
                neighbors.append(neighbor)

        if not cell.west:

            neighbor = Position(
                position.row,
                position.col - 1,
            )

            if self.valid_cell(neighbor) and not self.get_cell(neighbor).locked_42:
                neighbors.append(neighbor)

        return neighbors

    def reset_visited(self) -> None:
        """Clear traversal state so the maze can be explored again."""

        for row in self.grid:
            for cell in row:
                cell.visited = False
        
    def _lock_42_pattern(self) -> None:
        """Place the selected pattern at the centre of the maze."""
        pattern_height = len(self.pattern)
        pattern_width = max(len(row) for row in self.pattern)

        if self.rows < pattern_height or self.cols < pattern_width:
            raise ValueError(
                "maze is too small for the 42 pattern: "
                f"minimum size is {pattern_width}x{pattern_height}"
            )

        start_row = (self.rows - pattern_height) // 2
        start_col = (self.cols - pattern_width) // 2

        for pattern_row, line in enumerate(self.pattern):
            for pattern_col, mark in enumerate(line):
                if mark != "#":
                    continue

                row = start_row + pattern_row
                col = start_col + pattern_col
                self.grid[row][col].locked_42 = True

    # def _lock_42_pattern(self) -> None:
    #     pattern_cells = self._scaled_42_pattern()

    #     pattern_height = len(pattern_cells)
    #     pattern_width = len(pattern_cells[0])
    #     start_row = (self.rows - pattern_height) // 2
    #     start_col = (self.cols - pattern_width) // 2

    #     for pattern_row, line in enumerate(pattern_cells):
    #         for pattern_col, mark in enumerate(line):
    #             if mark != "#":
    #                 continue

    #             row = start_row + pattern_row
    #             col = start_col + pattern_col
    #             self.grid[row][col].locked_42 = True

    # def _scaled_42_pattern(self) -> tuple[str, ...]:
    #     base_height = len(self.PATTERN_42)
    #     base_width = max(len(row) for row in self.PATTERN_42)

    #     if self.rows < base_height or self.cols < base_width:
    #         raise ValueError(
    #             "maze is too small for the 42 pattern: "
    #             f"minimum size is {base_width}x{base_height}"
    #         )

    #     row_margin = 2 if self.rows > base_height + 2 else 0
    #     col_margin = 2 if self.cols > base_width + 2 else 0
    #     scale = min(
    #         max(1, (self.rows - row_margin) // base_height),
    #         max(1, (self.cols - col_margin) // base_width),
    #     )

    #     scaled_rows: list[str] = []
    #     for row in self.PATTERN_42:
    #         padded_row = row.ljust(base_width)
    #         scaled_row = "".join(mark * scale for mark in padded_row)
    #         scaled_rows.extend([scaled_row] * scale)

    #     return tuple(scaled_rows)

    def _validated_marker(
        self,
        position: Position | None,
        default: Position,
        name: str,
    ) -> Position:
        marker_position = position if position is not None else default

        if not self.valid_cell(marker_position):
            raise ValueError(f"{name} must be inside the maze")

        if self.grid[marker_position.row][marker_position.col].locked_42:
            raise ValueError(f"{name} cannot be inside the 42 pattern")

        return marker_position
