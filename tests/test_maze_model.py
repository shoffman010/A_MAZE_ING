import pytest

from cell import Cell
from direction import Direction
from maze import Maze
from position import Position


@pytest.mark.parametrize(
    ("cell", "expected_hex"),
    [
        (Cell(north=True, east=True, south=True, west=True), "F"),
        (Cell(north=True, east=False, south=True, west=False), "5"),
        (Cell(north=False, east=False, south=False, west=False), "0"),
    ],
)
def test_cell_hex_value_encodes_closed_walls(cell: Cell, expected_hex: str) -> None:
    assert cell.hex_value == expected_hex


def test_position_move_returns_adjacent_position() -> None:
    position = Position(row=4, col=7)

    assert position.move(Direction.NORTH) == Position(row=3, col=7)
    assert position.move(Direction.EAST) == Position(row=4, col=8)
    assert position.move(Direction.SOUTH) == Position(row=5, col=7)
    assert position.move(Direction.WEST) == Position(row=4, col=6)


def test_remove_wall_opens_both_sides_between_adjacent_cells() -> None:
    maze = Maze(rows=8, cols=8, pattern_name="X")
    current = Position(row=0, col=0)
    neighbor = Position(row=0, col=1)

    maze.remove_wall(current, neighbor)

    assert maze.get_cell(current).east is False
    assert maze.get_cell(neighbor).west is False


def test_unknown_pattern_raises_helpful_error() -> None:
    with pytest.raises(ValueError, match="unknown pattern 'missing'"):
        Maze(rows=8, cols=8, pattern_name="missing")
