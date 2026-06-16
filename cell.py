from dataclasses import dataclass


@dataclass()
class Cell:
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True

    @property
    def hex_value(self) -> str:
        value = (
            self.north * 1 +
            self.east * 2 +
            self.south * 4 +
            self.west * 8
        )

        return format(value, "X")