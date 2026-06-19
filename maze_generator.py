from position import Position
from maze import Maze
import random


class MazeGenerator:
    
    def _get_not_visited_neighbors(
            self,
            maze: Maze,
            position: Position
    ) -> list[Position]:
        neighbors: list[Position] = []

        for neighbor in maze._get_neighbors(position):
            cell = maze._get_cell(neighbor)
            if not cell.visited and not cell.locked_42:
                neighbors.append(neighbor)
        return neighbors
    
    
    def _dfs(
    self,
    maze: Maze,
    position: Position, ) -> None:
        current = maze._get_cell(position)

        current.visited = True

        neighbors = self._get_not_visited_neighbors(
            maze,
            position,
        )

        random.shuffle(neighbors)

        for neighbor in neighbors:

            if maze._get_cell(neighbor).visited:
                continue

            maze._remove_wall(
                position,
                neighbor,
            )

            self._dfs(
                maze,
                neighbor,
            )



    def generate(
        self,
        maze: Maze,
    ) -> None:
    
        self._dfs(
            maze,
            maze.entry,
        )