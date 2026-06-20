from dataclasses import dataclass
from direction import Direction

@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def move(
        self,
        direction: Direction,
    ) -> "Position":

        row_offset, col_offset = direction.value

        return Position(
            self.row + row_offset,
            self.col + col_offset,
        )
