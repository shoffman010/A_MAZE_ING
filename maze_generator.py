import random
import sys

from maze import Maze
from position import Position

sys.setrecursionlimit(20000)


class MazeGenerator:
    """Generate perfect or imperfect mazes while preserving locked cells."""

    _MAX_ROOM_SHAPES = ((2, 4), (3, 3), (4, 2))

    def __init__(self, seed: int | None = None) -> None:
        """Initialize a generator with optional reproducible randomness.

        Parameters
        ----------
        seed : int or None, optional
            Seed for random choices. ``None`` uses system-provided randomness.
        """
        # Random(None) gets fresh system-provided randomness; a numeric seed
        # makes every random choice in this generator reproducible.
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
            If ``True``, produce a single-route maze. If ``False``, add a
            limited number of extra passages.
        """
        maze.reset_visited()
        self._dfs(
            maze,
            maze.entry,
        )

        if not perfect:
            self._add_imperfections(maze)

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

        # print(position, [str(n) for n in neighbors],)

        self._random.shuffle(neighbors)

        # print("after:", [str(n) for n in neighbors],)

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

    def _add_imperfections(self, maze: Maze) -> None:
        """Open limited extra passages without creating oversized rooms.

        Parameters
        ----------
        maze : Maze
            Already-carved maze to make imperfect in place.
        """
        candidates: list[tuple[Position, Position]] = []

        for row in range(maze.rows):
            for col in range(maze.cols):
                position = Position(row, col)
                if maze.get_cell(position).locked_42:
                    continue

                # Looking only east and south considers every shared wall once.
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

        # One extra connection turns the DFS tree into an imperfect maze.  More
        # are useful for variety, but a small cap keeps the maze corridor-like.
        additions = max(1, len(candidates) // 12)
        added = 0

        for position, neighbor in candidates:
            if added >= additions:
                break

            maze.remove_wall(position, neighbor)
            if self._has_oversized_room(maze):
                self._restore_wall(maze, position, neighbor)
                continue

            added += 1
