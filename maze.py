from cell import Cell


class Maze:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(cols)]
            for _ in range(rows)
        ]

    def get_cell(self, row: int, col: int) -> Cell:
        return self.grid[row][col]