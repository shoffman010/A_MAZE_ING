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
    
# Creating 42 in the middle of the maze. Size maybe also varies depending on total maze size?
# All Cells that are making the 42, should be closed in the class cell.
# Using only 0x2588 from unicode.