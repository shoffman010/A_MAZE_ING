from maze import Maze
from maze_generator import MazeGenerator
from position import Position


def _graph_stats(maze: Maze) -> tuple[int, int, int]:
    positions: list[Position] = []
    edge_count = 0
    dead_ends = 0

    for row in range(maze.rows):
        for col in range(maze.cols):
            position = Position(row, col)
            if maze.get_cell(position).locked_42:
                continue
            degree = len(maze.get_reachable_neighbors(position))
            positions.append(position)
            edge_count += degree
            if degree == 1:
                dead_ends += 1

    edge_count //= 2
    components = 0
    seen: set[Position] = set()

    for position in positions:
        if position in seen:
            continue
        components += 1
        stack = [position]
        seen.add(position)

        while stack:
            current = stack.pop()
            for neighbor in maze.get_reachable_neighbors(current):
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                stack.append(neighbor)

    cycle_count = edge_count - len(positions) + components
    return components, cycle_count, dead_ends


def test_perfect_maze_has_one_component_and_no_loops() -> None:
    maze = Maze(
        rows=15,
        cols=30,
        pattern_name="42",
        entry=Position(1, 1),
        exit=Position(14, 29),
    )

    MazeGenerator(seed=42).generate(maze, perfect=True)

    components, cycle_count, _ = _graph_stats(maze)
    assert components == 1
    assert cycle_count == 0


def test_default_board_is_braided_with_open_required_cells() -> None:
    maze = Maze(
        rows=15,
        cols=30,
        pattern_name="42",
        entry=Position(1, 1),
        exit=Position(14, 29),
    )

    MazeGenerator(seed=42).generate(maze, perfect=False)

    components, cycle_count, dead_ends = _graph_stats(maze)
    assert components == 1
    assert cycle_count >= 2
    assert dead_ends == 0

    for position in maze.required_open_positions():
        assert not maze.get_cell(position).locked_42
        assert len(maze.get_reachable_neighbors(position)) >= 2


def test_impossible_playable_board_is_rejected() -> None:
    maze = Maze(
        rows=10,
        cols=10,
        pattern_name="42",
        entry=Position(0, 0),
        exit=Position(9, 9),
    )

    try:
        MazeGenerator(seed=42).generate(maze, perfect=False)
    except ValueError as error:
        assert "dead-end-free playable board" in str(error)
    else:
        raise AssertionError("expected impossible playable board to fail")
