from dataclasses import dataclass


@dataclass()
class Cell:
    """Store wall and traversal state for one maze cell.

    Parameters
    ----------
    north, east, south, west : bool, default=True
        Whether the corresponding cell boundary contains a wall.
    visited : bool, default=False
        Whether a traversal algorithm has visited the cell.
    locked_42 : bool, default=False
        Whether the cell belongs to the protected central pattern.
    """

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True

    visited: bool = False
    locked_42: bool = False

    @property
    def hex_value(self) -> str:
        """Encode this cell's four walls as one uppercase hexadecimal digit.

        Returns
        -------
        str
            Hexadecimal encoding with north, east, south, and west mapped to
            bit values 1, 2, 4, and 8, respectively.
        """
        value = self.north * 1 + self.east * 2 + self.south * 4 + self.west * 8

        return format(value, "X")
