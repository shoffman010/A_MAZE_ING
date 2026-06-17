from cell import Cell
from position import Position


class Maze:
    PATTERN_42: tuple[str] = (
    "# # ###",
    "# #   #",
    "### ###",
    "  # #  ",
    "  # ###",
    )

    # Print the Grid, height x width
    #row = 0 and col = 0 = north + west Outer boarder
    #row = 0 and col = max north + east Outer boarder
    #row = max col = 0 = south + west Outer boarder
    #row = max col = max = south + east Outer boarder
    #all the above cannot be touched, or changed. could be tuples or somehow else not accessible
    #Then initialize to all true for the whole inner grid, later we remove the walls when we use DFS\

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(cols)]
            for _ in range(rows)
        ]

    def valid_cell(self, row: int, col: int) -> bool:
        return (
            0 <= row < self.rows
            and
            0 <= col < self.cols
        )

    def get_cell(self, row: int, col: int) -> Cell:
        return self.grid[row][col]
    
    def remove_wall(self,
                    current_row: int,
                    current_col: int,
                    next_row: int,
                    next_col: int) -> None:
        current = self.grid[current_row][current_col]
        neighbor = self.grid[next_row][next_col]

        if next_col == current_col - 1:
            neighbor.east = False
            current.west = False
        elif next_row == current_row - 1:
            neighbor.south = False
            current.north = False
        elif next_col == current_col + 1:
            neighbor.west = False
            current.east = False
        elif next_row == current_row + 1:
            current.south = False
            neighbor.north = False
    

    def get_neighbors(self, row, col) -> list[Position]:
        
        neighbors: list[Position] = []

        adjust_position = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]
        for adjust_row, adjust_col in adjust_position:
            new_row = row  + adjust_row
            new_col = col + adjust_col
            if self.valid_cell(new_row, new_col):
                neighbors.append(Position(row = new_row, col = new_col))

            return neighbors
