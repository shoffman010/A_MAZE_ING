from .cell import Cell
from .direction import Direction
from .position import Position


class Maze:
    """A grid maze with an untouchable, locked pattern."""

    PATTERNS = {
        "42": (
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
        "Box": (
            "######",
            "#    # ",
            "#    # ",
            "#    # ",
            "######",
        ),
    }

    def __init__(
        self,
        rows: int,
        cols: int,
        pattern_name: str,
        entry: Position | None = None,
        exit: Position | None = None,
    ):
        """Create a maze grid and reserve its centred protected pattern.

        Parameters
        ----------
        rows : int
            Number of maze rows.
        cols : int
            Number of maze columns.
        pattern_name : str
            Name of a pattern defined in :attr:`PATTERNS`.
        entry : Position, optional
            Entry cell; defaults to the top-left cell.
        exit : Position, optional
            Exit cell; defaults to the bottom-right cell.

        Raises
        ------
        ValueError
            If the pattern is unknown, does not fit, a marker is invalid, or
            both markers identify the same cell.
        """
        self.rows = rows
        self.cols = cols

        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(cols)] for _ in range(rows)
        ]
        if pattern_name not in self.PATTERNS:
            valid_patterns = ", ".join(self.PATTERNS.keys())

            raise ValueError(
                f"unknown pattern '{pattern_name}'. "
                f"Valid patterns: {valid_patterns}"
            )

        self.pattern = self.PATTERNS[pattern_name]

        self._lock_42_pattern(entry, exit)
        self.entry = self._validated_marker(
            entry,
            Position(0, 0),
            "entry"
        )
        self.exit = self._validated_marker(
            exit,
            Position(rows - 1, cols - 1),
            "exit",
        )

        if self.entry == self.exit:
            raise ValueError("entry and exit must be different cells")

    def valid_cell(self, position: Position) -> bool:
        """Return whether a position lies within this maze's grid.

        Parameters
        ----------
        position : Position
            Position to validate.

        Returns
        -------
        bool
            ``True`` when both position indices are in bounds.
        """
        return 0 <= position.row < self.rows and 0 <= position.col < self.cols

    def get_cell(self, position: Position) -> Cell:
        """Return the cell at a valid maze position.

        Parameters
        ----------
        position : Position
            Grid position of the requested cell.

        Returns
        -------
        Cell
            Cell stored at ``position``.
        """
        return self.grid[position.row][position.col]

    def required_open_positions(self) -> list[Position]:
        """Return cells that must stay open in the playable board mode.

        Returns
        -------
        list of Position
            The four corners and the board centre. Duplicates are removed for
            very small mazes where positions can overlap.
        """
        positions = [
            Position(0, 0),
            Position(0, self.cols - 1),
            Position(self.rows - 1, 0),
            Position(self.rows - 1, self.cols - 1),
            Position(self.rows // 2, self.cols // 2),
        ]
        unique_positions: list[Position] = []
        for position in positions:
            if position not in unique_positions:
                unique_positions.append(position)
        return unique_positions

    def required_corridor_positions(self) -> list[Position]:
        """Return required playable cells and their immediate corridors."""
        positions: list[Position] = []

        for position in self.required_open_positions():
            if position not in positions:
                positions.append(position)

            for direction in Direction:
                neighbor = position.move(direction)
                if self.valid_cell(neighbor) and neighbor not in positions:
                    positions.append(neighbor)

        return positions

    def remove_wall(self, current: Position, neighbor: Position) -> None:
        """Open the shared wall between two adjacent cells.

        Parameters
        ----------
        current : Position
            First cell bordering the wall.
        neighbor : Position
            Orthogonally adjacent cell bordering the same wall.
        """
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
        """Return in-bounds adjacent cells outside the protected pattern.

        Parameters
        ----------
        position : Position
            Cell whose neighbours are requested.

        Returns
        -------
        list of Position
            Orthogonally adjacent, unlocked positions; wall state is ignored.
        """

        neighbors: list[Position] = []

        # adjust_position = [
        #     (-1, 0),
        #     (1, 0),
        #     (0, -1),
        #     (0, 1)
        # ]
        for direction in Direction:
            new_neighbor = position.move(direction)
            if (
                self.valid_cell(new_neighbor)
                and not self.get_cell(new_neighbor).locked_42
            ):
                neighbors.append(new_neighbor)

        return neighbors

    def get_reachable_neighbors(
        self,
        position: Position,
    ) -> list[Position]:
        """Return unlocked neighbours connected through open walls.

        Parameters
        ----------
        position : Position
            Cell from which to inspect open passages.

        Returns
        -------
        list of Position
            Adjacent unlocked cells reachable directly from ``position``.
        """
        neighbors: list[Position] = []

        cell = self.get_cell(position)

        if not cell.north:

            neighbor = Position(
                position.row - 1,
                position.col,
            )

            if (
                self.valid_cell(neighbor)
                and not self.get_cell(neighbor).locked_42
            ):
                neighbors.append(neighbor)

        if not cell.east:

            neighbor = Position(
                position.row,
                position.col + 1,
            )

            if (
                self.valid_cell(neighbor)
                and not self.get_cell(neighbor).locked_42
            ):
                neighbors.append(neighbor)

        if not cell.south:

            neighbor = Position(
                position.row + 1,
                position.col,
            )

            if (
                self.valid_cell(neighbor)
                and not self.get_cell(neighbor).locked_42
            ):
                neighbors.append(neighbor)

        if not cell.west:

            neighbor = Position(
                position.row,
                position.col - 1,
            )

            if (
                self.valid_cell(neighbor)
                and not self.get_cell(neighbor).locked_42
            ):
                neighbors.append(neighbor)

        return neighbors

    def reset_visited(self) -> None:
        """Clear traversal state so the maze can be explored again.

        Returns
        -------
        None
        """

        for row in self.grid:
            for cell in row:
                cell.visited = False

    def _lock_42_pattern(
        self,
        entry: Position | None,
        exit: Position | None,
    ) -> None:
        """Mark the selected centred pattern as protected cells.

        Raises
        ------
        ValueError
            If the maze dimensions cannot contain the selected pattern.
        """
        pattern_height = len(self.pattern)
        pattern_width = max(len(row) for row in self.pattern)

        if self.rows < pattern_height or self.cols < pattern_width:
            raise ValueError(
                "maze is too small for the 42 pattern: "
                f"minimum size is {pattern_width}x{pattern_height}"
            )

        start_row, start_col = self._find_pattern_origin(
            pattern_height,
            pattern_width,
        )

        for pattern_row, line in enumerate(self.pattern):
            for pattern_col, mark in enumerate(line):
                if mark != "#":
                    continue

                row = start_row + pattern_row
                col = start_col + pattern_col
                self.grid[row][col].locked_42 = True
                self.grid[row][col].pattern_42 = True

        self._lock_pattern_pockets(entry, exit)

    def _lock_pattern_pockets(
        self,
        entry: Position | None,
        exit: Position | None,
    ) -> None:
        """Absorb pattern-created cul-de-sacs into the closed pattern.

        Parameters
        ----------
        entry, exit : Position or None
            Markers that must not be absorbed into the protected pattern.
        """
        protected_positions = set(self.required_corridor_positions())
        for marker in (entry, exit):
            if marker is not None and self.valid_cell(marker):
                protected_positions.add(marker)

        changed = True
        while changed:
            changed = False

            for row in range(self.rows):
                for col in range(self.cols):
                    position = Position(row, col)
                    cell = self.grid[row][col]
                    if cell.locked_42 or position in protected_positions:
                        continue

                    if self._unlocked_neighbor_count(position) <= 1:
                        cell.locked_42 = True
                        changed = True

    def _unlocked_neighbor_count(self, position: Position) -> int:
        """Return how many adjacent cells are available as corridors."""
        count = 0

        for direction in Direction:
            neighbor = position.move(direction)
            if (
                self.valid_cell(neighbor)
                and not self.grid[neighbor.row][neighbor.col].locked_42
            ):
                count += 1
        return count

    def _find_pattern_origin(
        self,
        pattern_height: int,
        pattern_width: int,
    ) -> tuple[int, int]:
        """Choose the nearest centred position that keeps key cells open.

        Parameters
        ----------
        pattern_height, pattern_width : int
            Dimensions of the selected pattern.

        Returns
        -------
        tuple of int
            Top-left pattern origin as ``(row, column)``.
        """
        preferred_row = (self.rows - pattern_height) // 2
        preferred_col = (self.cols - pattern_width) // 2
        origins: list[tuple[int, int]] = []

        for row in range(self.rows - pattern_height + 1):
            for col in range(self.cols - pattern_width + 1):
                origins.append((row, col))

        origins.sort(
            key=lambda origin: (
                abs(origin[0] - preferred_row)
                + abs(origin[1] - preferred_col),
                self._pattern_required_open_overlap_count(
                    origin[0],
                    origin[1],
                ),
            )
        )

        for origin in origins:
            if self._pattern_keeps_required_corridors_open(*origin):
                return origin

        return origins[0]

    def _pattern_keeps_required_corridors_open(
        self,
        start_row: int,
        start_col: int,
    ) -> bool:
        """Return whether required cells stay open corridor candidates."""
        pattern_positions = self._pattern_positions(start_row, start_col)

        for position in self.required_open_positions():
            if position in pattern_positions:
                return False

            available_neighbors = 0
            for direction in Direction:
                neighbor = position.move(direction)
                if (
                    self.valid_cell(neighbor)
                    and neighbor not in pattern_positions
                ):
                    available_neighbors += 1

            if available_neighbors < min(2, len(self.get_neighbors(position))):
                return False

        return True

    def _pattern_required_open_overlap_count(
        self,
        start_row: int,
        start_col: int,
    ) -> int:
        """Return how many required open cells a pattern would lock."""
        required_positions = set(self.required_open_positions())
        overlap_count = 0

        for position in self._pattern_positions(start_row, start_col):
            if position in required_positions:
                overlap_count += 1
        return overlap_count

    def _pattern_positions(
        self,
        start_row: int,
        start_col: int,
    ) -> set[Position]:
        """Return positions occupied by the selected pattern at an origin."""
        positions: set[Position] = set()

        for pattern_row, line in enumerate(self.pattern):
            for pattern_col, mark in enumerate(line):
                if mark == "#":
                    positions.add(
                        Position(
                            start_row + pattern_row,
                            start_col + pattern_col,
                        )
                    )

        return positions

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
        """Return a valid, unlocked marker position.

        Parameters
        ----------
        position : Position or None
            User-supplied marker position, if any.
        default : Position
            Position to use when ``position`` is ``None``.
        name : str
            Marker name used in validation error messages.

        Returns
        -------
        Position
            Validated marker position.

        Raises
        ------
        ValueError
            If the marker is outside the maze or within the protected pattern.
        """
        marker_position = position if position is not None else default

        if not self.valid_cell(marker_position):
            raise ValueError(f"{name} must be inside the maze")

        if self.grid[marker_position.row][marker_position.col].locked_42:
            raise ValueError(f"{name} cannot be inside the 42 pattern")

        return marker_position
