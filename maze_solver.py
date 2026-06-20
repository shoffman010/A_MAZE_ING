from collections import deque

from maze import Maze
from position import Position


class MazeSolver:

    def _reconstruct_path(
    self,
    parents: dict[
        Position,
        Position | None,
    ],
    goal: Position,
) -> list[Position]:

        path: list[Position] = []

        current: Position | None = goal

        while current is not None:

            path.append(current)

            current = parents[current]

        path.reverse()

        return path

    def solve(
        self,
        maze: Maze,
    ) -> list[Position]:

        maze.reset_visited()

        cell_queue = deque([maze.entry])

        maze.get_cell(maze.entry).visited = True

        parents: dict[Position, Position | None,] = {maze.entry: None}

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
        return self._reconstruct_path(parents, maze.exit,)