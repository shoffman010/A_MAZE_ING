import random
import sys

from .maze import Maze
from .position import Position

sys.setrecursionlimit(20000)


class MazeGenerator:
    """Generate maze passages while preserving protected pattern cells.

    A depth-first traversal creates the initial perfect maze. Optional
    post-processing adds loops and removes dead ends to create the default
    Pac-Man-like playable board.
    """

    _MAX_ROOM_SHAPES = ((2, 4), (3, 3), (4, 2))
    _MIN_PLAYABLE_LOOPS = 2

    def __init__(self, seed: int | None = None) -> None:
        """Initialize a generator with optional reproducible randomness.

        Parameters
        ----------
        seed : int or None, optional
            Seed for random choices. ``None`` uses system-provided randomness.
        """
        self._random = random.Random(seed)

    def generate(
        self,
        maze: Maze,
        perfect: bool = True,
    ) -> None:
        """Carve a maze, optionally adding passages to make it imperfect.

        Parameters
        ----------
        maze : Maze
            Initialized maze to carve in place.
        perfect : bool, default=True
            If ``True``, produce a single-route maze. If ``False``, braid the
            maze into a Pac-Man-like board with multiple routes.
        """
        maze.reset_visited()
        self._dfs(
            maze,
            maze.entry,
        )

        if not perfect:
            self._make_playable_board(maze)

    def _get_not_visited_neighbors(
        self, maze: Maze, position: Position
    ) -> list[Position]:
        """Return adjacent unlocked cells that have not been visited.

        Parameters
        ----------
        maze : Maze
            Maze containing the cells.
        position : Position
            Cell from which to inspect neighbours.

        Returns
        -------
        list of Position
            Unvisited neighbours eligible for depth-first carving.
        """
        neighbors: list[Position] = []

        for neighbor in maze.get_neighbors(position):
            cell = maze.get_cell(neighbor)
            if not cell.visited:
                neighbors.append(neighbor)
        return neighbors

    def _dfs(
        self,
        maze: Maze,
        position: Position,
    ) -> None:
        """Recursively carve a depth-first spanning tree from a cell.

        Parameters
        ----------
        maze : Maze
            Maze to mutate.
        position : Position
            Starting cell for this recursive carving step.
        """
        current = maze.get_cell(position)

        current.visited = True

        neighbors = self._get_not_visited_neighbors(
            maze,
            position,
        )

        self._random.shuffle(neighbors)

        for neighbor in neighbors:

            if maze.get_cell(neighbor).visited:
                continue

            maze.remove_wall(
                position,
                neighbor,
            )

            self._dfs(
                maze,
                neighbor,
            )

    def _is_open_rectangle(
        self,
        maze: Maze,
        top: int,
        left: int,
        height: int,
        width: int,
    ) -> bool:
        """Return whether every internal wall in a cell rectangle is open.

        Parameters
        ----------
        maze : Maze
            Maze to inspect.
        top, left : int
            Row and column of the rectangle's top-left cell.
        height, width : int
            Rectangle dimensions in cells.

        Returns
        -------
        bool
            ``True`` if the rectangle has no protected cells or internal walls.
        """
        for row in range(top, top + height):
            for col in range(left, left + width):
                position = Position(row, col)
                cell = maze.get_cell(position)

                if cell.locked_42:
                    return False

                if col < left + width - 1 and cell.east:
                    return False
                if row < top + height - 1 and cell.south:
                    return False

        return True

    def _has_oversized_room(self, maze: Maze) -> bool:
        """Return whether an open room exceeds the permitted size.

        Parameters
        ----------
        maze : Maze
            Maze to inspect for open rectangular rooms.

        Returns
        -------
        bool
            ``True`` if an open 2x4, 3x3, or 4x2 rectangle exists.
        """
        for height, width in self._MAX_ROOM_SHAPES:
            for top in range(maze.rows - height + 1):
                for left in range(maze.cols - width + 1):
                    if self._is_open_rectangle(maze, top, left, height, width):
                        return True
        return False

    def _restore_wall(
        self,
        maze: Maze,
        current: Position,
        neighbor: Position,
    ) -> None:
        """Restore the shared wall between two adjacent cells.

        Parameters
        ----------
        maze : Maze
            Maze to mutate.
        current, neighbor : Position
            Orthogonally adjacent cells on either side of the wall.
        """
        current_cell = maze.get_cell(current)
        neighbor_cell = maze.get_cell(neighbor)

        if neighbor.col == current.col - 1:
            current_cell.west = True
            neighbor_cell.east = True
        elif neighbor.row == current.row - 1:
            current_cell.north = True
            neighbor_cell.south = True
        elif neighbor.col == current.col + 1:
            current_cell.east = True
            neighbor_cell.west = True
        elif neighbor.row == current.row + 1:
            current_cell.south = True
            neighbor_cell.north = True

    def _get_closed_neighbors(
        self,
        maze: Maze,
        position: Position,
    ) -> list[Position]:
        """Return adjacent unlocked cells separated by a closed wall.

        Parameters
        ----------
        maze : Maze
            Maze containing the cells.
        position : Position
            Cell whose closed neighbouring walls are inspected.

        Returns
        -------
        list of Position
            Valid unlocked neighbours not directly reachable from ``position``.
        """
        reachable = set(maze.get_reachable_neighbors(position))

        return [
            neighbor
            for neighbor in maze.get_neighbors(position)
            if neighbor not in reachable
        ]

    def _try_remove_wall(
        self,
        maze: Maze,
        position: Position,
        neighbor: Position,
    ) -> bool:
        """Open a wall only when the resulting board remains corridor-like.

        Parameters
        ----------
        maze : Maze
            Maze to mutate.
        position, neighbor : Position
            Adjacent cells whose shared wall may be opened.

        Returns
        -------
        bool
            ``True`` when the wall stayed open, otherwise ``False``.
        """
        maze.remove_wall(position, neighbor)
        if self._has_oversized_room(maze):
            self._restore_wall(maze, position, neighbor)
            return False
        return True

    def _cell_degree(
        self,
        maze: Maze,
        position: Position,
    ) -> int:
        """Count the open passages connected to a cell.

        Args:
            maze: Maze containing the cell and its carved passages.
            position: Position of the cell to inspect.

        Returns:
            Number of directly reachable neighbouring cells.
        """
        return len(maze.get_reachable_neighbors(position))

    def _unlocked_positions(self, maze: Maze) -> list[Position]:
        """Collect positions outside the protected pattern.

        Args:
            maze: Maze whose cells will be inspected.

        Returns:
            Every position that remains available for maze passages.
        """
        positions: list[Position] = []

        for row in range(maze.rows):
            for col in range(maze.cols):
                position = Position(row, col)
                if not maze.get_cell(position).locked_42:
                    positions.append(position)
        return positions

    def _dead_ends(self, maze: Maze) -> list[Position]:
        """Find unlocked cells with only one open passage.

        Args:
            maze: Carved maze to inspect.

        Returns:
            Positions whose passage degree is exactly one.
        """
        return [
            position
            for position in self._unlocked_positions(maze)
            if self._cell_degree(maze, position) == 1
        ]

    def _cycle_count(self, maze: Maze) -> int:
        """Return the independent loop count of the open maze graph.

        Returns
        -------
        int
            Cyclomatic number: open edges minus unlocked cells plus connected
            components.
        """
        positions = self._unlocked_positions(maze)
        position_set = set(positions)
        edge_count = 0
        components = 0
        seen: set[Position] = set()

        for position in positions:
            edge_count += self._cell_degree(maze, position)
        edge_count //= 2

        for position in positions:
            if position in seen:
                continue
            components += 1
            stack = [position]
            seen.add(position)
            while stack:
                current = stack.pop()
                for neighbor in maze.get_reachable_neighbors(current):
                    if neighbor not in position_set or neighbor in seen:
                        continue
                    seen.add(neighbor)
                    stack.append(neighbor)

        return edge_count - len(positions) + components

    def _open_required_corridors(self, maze: Maze) -> None:
        """Open enough walls around required playable-board cells.

        Args:
            maze: Maze to modify in place.

        Raises:
            ValueError: If a required playable cell belongs to the protected
                pattern.
        """
        for position in maze.required_open_positions():
            if maze.get_cell(position).locked_42:
                raise ValueError("required playable-board cell is locked")

            target_degree = min(2, len(maze.get_neighbors(position)))
            attempts = 0

            while (
                self._cell_degree(maze, position) < target_degree
                and attempts < maze.rows * maze.cols
            ):
                attempts += 1
                candidates = self._get_closed_neighbors(maze, position)
                if not candidates:
                    break
                candidates.sort(
                    key=lambda neighbor: self._cell_degree(maze, neighbor)
                )

                opened = False
                for neighbor in candidates:
                    if self._try_remove_wall(maze, position, neighbor):
                        opened = True
                        break

                if not opened:
                    break

    def _open_extra_loops(self, maze: Maze) -> None:
        """Add the minimum independent loops required by playable mode.

        Args:
            maze: Maze to modify in place.

        Candidate walls are shuffled before opening so seeded generation stays
        reproducible without producing the same structure for every seed.
        """
        candidates: list[tuple[Position, Position]] = []

        for row in range(maze.rows):
            for col in range(maze.cols):
                position = Position(row, col)
                if maze.get_cell(position).locked_42:
                    continue

                for neighbor in (
                    Position(row, col + 1),
                    Position(row + 1, col),
                ):
                    if not maze.valid_cell(neighbor):
                        continue
                    if maze.get_cell(neighbor).locked_42:
                        continue
                    if neighbor in maze.get_reachable_neighbors(position):
                        continue
                    candidates.append((position, neighbor))

        self._random.shuffle(candidates)

        for position, neighbor in candidates:
            if self._cycle_count(maze) >= self._MIN_PLAYABLE_LOOPS:
                break
            self._try_remove_wall(maze, position, neighbor)

    def _braid_dead_ends(self, maze: Maze) -> None:
        """Remove dead ends by opening safe neighbouring walls.

        Args:
            maze: Maze to modify in place.

        The process stops after two stalled rounds so layouts that cannot be
        improved do not loop indefinitely.
        """
        stalled_rounds = 0
        previous_dead_end_count = len(self._dead_ends(maze))

        while previous_dead_end_count and stalled_rounds < 2:
            dead_ends = self._dead_ends(maze)
            self._random.shuffle(dead_ends)
            opened_any = False

            for position in dead_ends:
                if self._cell_degree(maze, position) != 1:
                    continue

                candidates = self._get_closed_neighbors(maze, position)
                self._random.shuffle(candidates)
                candidates.sort(
                    key=lambda neighbor: self._cell_degree(maze, neighbor)
                )

                for neighbor in candidates:
                    if self._try_remove_wall(maze, position, neighbor):
                        opened_any = True
                        break

            current_dead_end_count = len(self._dead_ends(maze))
            if (
                not opened_any
                or current_dead_end_count >= previous_dead_end_count
            ):
                stalled_rounds += 1
            else:
                stalled_rounds = 0
            previous_dead_end_count = current_dead_end_count

    def _make_playable_board(self, maze: Maze) -> None:
        """Braid a DFS maze into the default Pac-Man-like board.

        Parameters
        ----------
        maze : Maze
            Already-carved maze to make playable in place.
        """
        self._validate_playable_board_space(maze)
        self._open_required_corridors(maze)
        self._open_extra_loops(maze)
        self._braid_dead_ends(maze)
        self._open_required_corridors(maze)

    def _validate_playable_board_space(self, maze: Maze) -> None:
        """Validate that required cells can form playable corridors.

        Args:
            maze: Maze layout to validate.

        Raises:
            ValueError: If a required cell is locked or has fewer than two
                available neighbours.
        """
        for position in maze.required_open_positions():
            if maze.get_cell(position).locked_42:
                raise ValueError("required playable-board cell is locked")
            if len(maze.get_neighbors(position)) < 2:
                raise ValueError(
                    "maze is too small for a dead-end-free playable board"
                )
