from position import Position
from maze import Maze
import random
import sys

sys.setrecursionlimit(20000)

class MazeGenerator:
    
    def _get_not_visited_neighbors(
            self,
            maze: Maze,
            position: Position
    ) -> list[Position]:
        neighbors: list[Position] = []

        for neighbor in maze.get_neighbors(position):
            cell = maze.get_cell(neighbor)
            if not cell.visited:
                neighbors.append(neighbor)
        return neighbors
    
    
    def _dfs(
    self,
    maze: Maze,
    position: Position, ) -> None:
        current = maze.get_cell(position)

        current.visited = True

        neighbors = self._get_not_visited_neighbors(
            maze,
            position,
        )

        # print(position, [str(n) for n in neighbors],)

        random.shuffle(neighbors)

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



    def generate(
        self,
        maze: Maze,
    ) -> None:
    
        self._dfs(
            maze,
            maze.entry,
        )
