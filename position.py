from dataclasses import dataclass
from direction import Direction


@dataclass(frozen=True)
class Position:
    """Represent an immutable zero-based cell position in a maze.

    Parameters
    ----------
    row : int
        Vertical cell index.
    col : int
        Horizontal cell index.
    """

    row: int
    col: int

    def move(
        self,
        direction: Direction,
    ) -> "Position":
        """Return the adjacent position in ``direction``.

        Parameters
        ----------
        direction : Direction
            Cardinal direction in which to move.

        Returns
        -------
        Position
            A new position offset by one cell. Bounds are not checked.
        """

        row_offset, col_offset = direction.value

        return Position(
            self.row + row_offset,
            self.col + col_offset,
        )
