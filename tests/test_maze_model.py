"""Unit tests for the small maze model building blocks."""

import pytest

from mazegen import Cell, Direction, Maze, Position


@pytest.mark.parametrize(
    ("cell", "expected_hex"),
    [
        # North, east, south, and west map to bit values 1, 2, 4, and 8.
        (Cell(north=False, east=False, south=False, west=False), "0"),
        (Cell(north=True, east=False, south=False, west=False), "1"),
        (Cell(north=False, east=True, south=False, west=False), "2"),
        (Cell(north=True, east=True, south=False, west=False), "3"),
        (Cell(north=False, east=False, south=True, west=False), "4"),
        (Cell(north=True, east=False, south=True, west=False), "5"),
        (Cell(north=False, east=True, south=True, west=False), "6"),
        (Cell(north=True, east=True, south=True, west=False), "7"),
        (Cell(north=False, east=False, south=False, west=True), "8"),
        (Cell(north=True, east=False, south=False, west=True), "9"),
        (Cell(north=False, east=True, south=False, west=True), "A"),
        (Cell(north=True, east=True, south=False, west=True), "B"),
        (Cell(north=False, east=False, south=True, west=True), "C"),
        (Cell(north=True, east=False, south=True, west=True), "D"),
        (Cell(north=False, east=True, south=True, west=True), "E"),
        (Cell(north=True, east=True, south=True, west=True), "F"),
    ],
)
def test_cell_hex_value_encodes_closed_walls(
    cell: Cell,
    expected_hex: str,
) -> None:
    """Check every wall combination maps to the required hex digit."""
    assert cell.hex_value == expected_hex


def test_position_move_returns_adjacent_position() -> None:
    """Check that moving one step applies the direction row/column offset."""
    position = Position(row=4, col=7)

    assert position.move(Direction.NORTH) == Position(row=3, col=7)
    assert position.move(Direction.EAST) == Position(row=4, col=8)
    assert position.move(Direction.SOUTH) == Position(row=5, col=7)
    assert position.move(Direction.WEST) == Position(row=4, col=6)


def test_remove_wall_opens_both_sides_between_adjacent_cells() -> None:
    """Check that removing a shared wall updates both neighbouring cells."""
    maze = Maze(rows=8, cols=8, pattern_name="X")
    current = Position(row=0, col=0)
    neighbor = Position(row=0, col=1)

    maze.remove_wall(current, neighbor)

    assert maze.get_cell(current).east is False
    assert maze.get_cell(neighbor).west is False


def test_visible_pattern_is_centered_without_locked_pocket_expansion() -> None:
    """Check the rendered 42 shape stays separate from extra locked cells."""
    maze = Maze(rows=20, cols=30, pattern_name="42")

    visible_pattern = [
        "".join("#" if cell.pattern_42 else "." for cell in row)
        for row in maze.grid
    ]

    assert visible_pattern[7:12] == [
        "............#.#.###...........",
        "............#.#...#...........",
        "............###.###...........",
        "..............#.#.............",
        "..............#.###...........",
    ]
    assert not maze.get_cell(Position(row=10, col=15)).locked_42
    assert any(
        cell.locked_42 and not cell.pattern_42
        for row in maze.grid
        for cell in row
    )


def test_unknown_pattern_raises_helpful_error() -> None:
    """Check invalid pattern names fail with a useful message."""
    with pytest.raises(ValueError, match="unknown pattern 'missing'"):
        Maze(rows=8, cols=8, pattern_name="missing")
