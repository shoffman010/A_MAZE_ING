from position import Position
from maze import Maze

class MazeGenerator:
    def get_not_visited_neighbors(self, maze: Maze, row: int, col: int) -> list[Position]:
        neighbors: list[Position] = []

        for position in maze.get_neighbors(row, col):
            cell = maze.grid[position.row][position.col]
            if not cell.visited:
                neighbors.add(position)
        return neighbors