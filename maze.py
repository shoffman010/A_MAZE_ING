from cell import Cell


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

    def get_cell(self, row: int, col: int) -> Cell:
        return self.grid[row][col]