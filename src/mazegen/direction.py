from enum import Enum


class Direction(Enum):
    """Represent a cardinal direction as a row and column offset.

    Each member stores the offset needed to move one cell in that direction.
    Negative rows move north and negative columns move west.
    """
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
