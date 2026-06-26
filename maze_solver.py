from collections import deque

from maze import Maze
from position import Position
import time
from renderer import Renderer


class MazeSolver:
    """Find routes through carved maze passages."""

    def solve(
        self,
        maze: Maze,
    ) -> list[Position]:
        """Return the shortest open route from the entry to the exit.

        Parameters
        ----------
        maze : Maze
            Carved maze containing entry and exit markers.

        Returns
        -------
        list of Position
            Positions on the shortest route, ordered from entry to exit.
        """
        
        maze.reset_visited()

        cell_queue = deque([maze.entry])

        maze.get_cell(maze.entry).visited = True

        parents: dict[
            Position,
            Position | None,
        ] = {maze.entry: None}

        while cell_queue:
            current_cell = cell_queue.popleft()
            if current_cell == maze.exit:
                break

            for neighbor in maze.get_reachable_neighbors(current_cell):
                neighbor_cell = maze.get_cell(neighbor)
                if neighbor_cell.visited:
                    continue
                neighbor_cell.visited = True
                parents[neighbor] = current_cell
                cell_queue.append(neighbor)
        return self._reconstruct_path(
            parents,
            maze.exit,
        )
        
    def _reconstruct_path(
        self,
        parents: dict[
            Position,
            Position | None,
        ],
        goal: Position,
    ) -> list[Position]:
        """Build an entry-to-goal route from breadth-first parent links.

        Parameters
        ----------
        parents : dict of Position to Position or None
            Predecessor map rooted at the maze entry.
        goal : Position
            Final position whose route should be reconstructed.

        Returns
        -------
        list of Position
            Reconstructed route ordered from the root to ``goal``.
        """
        path: list[Position] = []

        current: Position | None = goal

        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()

        return path
