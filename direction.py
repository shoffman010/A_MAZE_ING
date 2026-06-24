from enum import Enum


class Direction(Enum):
    """Enumerate the four cardinal one-cell movement offsets."""
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
