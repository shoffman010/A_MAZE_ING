"""Subject-level tests for configuration, output, and analyzer constraints."""

import subprocess
import sys
from pathlib import Path

import pytest

from mazegen import Maze, MazeGenerator, MazeSolver, MazeWriter, Position
from mazegen.config import Config, load_config
from tools import maze_analyzer


def _build_maze(
    *,
    rows: int = 20,
    cols: int = 30,
    perfect: bool = False,
    seed: int | None = 42,
) -> Maze:
    """Create a generated 42 maze for subject-level assertions.

    Parameters
    ----------
    rows, cols : int, default=20, 30
        Maze dimensions in cells.
    perfect : bool, default=False
        Whether to generate the perfect-maze mode or Pac-Man board mode.
    seed : int or None, default=42
        Seed passed to the generator for reproducible tests.

    Returns
    -------
    Maze
        Generated maze with the same entry and exit used by the default config.
    """
    maze = Maze(
        rows=rows,
        cols=cols,
        pattern_name="42",
        entry=Position(1, 1),
        exit=Position(14, 29),
    )

    MazeGenerator(seed=seed).generate(maze, perfect=perfect)
    return maze


def _write_output(maze: Maze, output_file: Path) -> None:
    """Serialize a generated maze with its shortest solution path.

    Parameters
    ----------
    maze : Maze
        Maze to solve and write.
    output_file : Path
        Destination file used by the test.
    """
    path = MazeSolver().solve(maze)
    MazeWriter().write_maze(maze, path, str(output_file))


def _grid_hex(maze: Maze) -> list[str]:
    """Return the maze grid in the same hex format as the output file.

    Parameters
    ----------
    maze : Maze
        Maze whose cells should be encoded.

    Returns
    -------
    list of str
        One uppercase hexadecimal row per maze row.
    """
    return [
        "".join(cell.hex_value for cell in row)
        for row in maze.grid
    ]


def _open_rectangle_exists(
    maze: Maze,
    height: int,
    width: int,
) -> bool:
    """Return whether a fully open rectangle exists in the maze.

    Parameters
    ----------
    maze : Maze
        Generated maze to inspect.
    height, width : int
        Rectangle dimensions to scan for.

    Returns
    -------
    bool
        ``True`` when all internal walls in a rectangle are open.
    """
    generator = MazeGenerator(seed=0)
    for top in range(maze.rows - height + 1):
        for left in range(maze.cols - width + 1):
            if generator._is_open_rectangle(maze, top, left, height, width):
                return True
    return False


def _config_file(tmp_path: Path, text: str) -> Path:
    """Write temporary config text and return its path.

    Parameters
    ----------
    tmp_path : Path
        Pytest-provided temporary directory.
    text : str
        Config file content to write.

    Returns
    -------
    Path
        Path to the generated temporary config file.
    """
    path = tmp_path / "config.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_config_accepts_subject_keys_comments_and_optional_defaults(
    tmp_path: Path,
) -> None:
    """Check mandatory subject keys and optional defaults.

    The subject allows comments and additional optional keys. This test keeps
    the minimal mandatory config working while confirming local defaults.
    """
    path = _config_file(
        tmp_path,
        """
        # subject-style config
        WIDTH=30
        HEIGHT=20
        ENTRY=1,1
        EXIT=29,14
        OUTPUT_FILE=maze.txt
        PERFECT=False
        """,
    )

    config = load_config(str(path))

    assert config == Config(
        width=30,
        height=20,
        entry=(1, 1),
        exit=(14, 29),
        perfect=False,
        output_file="maze.txt",
        pattern="42",
        seed=None,
        wall_color="DEFAULT",
        path_color="RED",
        pattern_color="CYAN",
    )


@pytest.mark.parametrize(
    ("text", "message"),
    [
        (
            """
            HEIGHT=20
            ENTRY=1,1
            EXIT=29,14
            OUTPUT_FILE=maze.txt
            PERFECT=False
            """,
            "missing required config key",
        ),
        (
            """
            WIDTH=30
            HEIGHT=20
            ENTRY=1,1
            EXIT=29,14
            OUTPUT_FILE=maze.txt
            PERFECT=False
            PERFECT=True
            """,
            "duplicate config key: PERFECT",
        ),
        (
            """
            WIDTH=30
            HEIGHT=20
            ENTRY=1,1
            EXIT=29,14
            OUTPUT_FILE=maze.txt
            PERFECT=false
            """,
            "PERFECT must be True or False",
        ),
        (
            """
            WIDTH=30
            HEIGHT=20
            ENTRY=30,1
            EXIT=29,14
            OUTPUT_FILE=maze.txt
            PERFECT=False
            """,
            "ENTRY must be inside the maze bounds",
        ),
    ],
)
def test_config_rejects_invalid_subject_parameters(
    tmp_path: Path,
    text: str,
    message: str,
) -> None:
    """Check invalid subject parameters are rejected with clear messages."""
    path = _config_file(tmp_path, text)

    with pytest.raises(ValueError, match=message):
        load_config(str(path))


def test_program_reports_bad_config_without_traceback(tmp_path: Path) -> None:
    """Check the CLI reports config errors gracefully instead of crashing."""
    path = _config_file(
        tmp_path,
        """
        WIDTH=0
        HEIGHT=20
        ENTRY=1,1
        EXIT=29,14
        OUTPUT_FILE=maze.txt
        PERFECT=False
        """,
    )

    result = subprocess.run(
        [sys.executable, "a_maze_ing.py", str(path)],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1
    assert "Error: WIDTH must be greater than 0" in result.stderr
    assert "Traceback" not in result.stderr


def test_same_seed_recreates_the_same_maze() -> None:
    """Check the required seed reproducibility behavior."""
    first = _build_maze(seed=12345)
    second = _build_maze(seed=12345)

    assert _grid_hex(first) == _grid_hex(second)


def test_maze_keeps_external_borders_closed() -> None:
    """Check the outside border walls stay closed around the full maze."""
    maze = _build_maze()

    for col in range(maze.cols):
        assert maze.get_cell(Position(0, col)).north
        assert maze.get_cell(Position(maze.rows - 1, col)).south

    for row in range(maze.rows):
        assert maze.get_cell(Position(row, 0)).west
        assert maze.get_cell(Position(row, maze.cols - 1)).east


def test_maze_has_coherent_shared_walls() -> None:
    """Check neighbouring cells agree on every shared wall."""
    maze = _build_maze()

    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze.get_cell(Position(row, col))
            if col < maze.cols - 1:
                east = maze.get_cell(Position(row, col + 1))
                assert cell.east == east.west
            if row < maze.rows - 1:
                south = maze.get_cell(Position(row + 1, col))
                assert cell.south == south.north


def test_default_board_has_no_oversized_open_areas() -> None:
    """Check default boards do not contain forbidden large open rooms."""
    maze = _build_maze(perfect=False)

    assert not _open_rectangle_exists(maze, 3, 3)
    assert not _open_rectangle_exists(maze, 2, 4)
    assert not _open_rectangle_exists(maze, 4, 2)


def test_too_small_maze_rejects_required_42_pattern() -> None:
    """Check mazes too small for the visible 42 fail with an error."""
    with pytest.raises(
        ValueError,
        match="maze is too small for the 42 pattern",
    ):
        Maze(rows=4, cols=6, pattern_name="42")


def test_output_file_uses_hex_grid_footer_and_shortest_path(
    tmp_path: Path,
) -> None:
    """Check the subject output format: grid, blank line, footer, and path."""
    maze = _build_maze(seed=42)
    output_file = tmp_path / "maze.txt"
    _write_output(maze, output_file)

    lines = output_file.read_text(encoding="utf-8").splitlines()
    blank_index = lines.index("")
    grid = lines[:blank_index]
    entry, exit_, path = lines[blank_index + 1:]

    assert len(grid) == maze.rows
    assert all(len(row) == maze.cols for row in grid)
    assert all(char in "0123456789ABCDEF" for row in grid for char in row)
    assert entry == "1,1"
    assert exit_ == "29,14"
    assert set(path) <= {"N", "E", "S", "W"}
    assert len(path) == len(MazeSolver().solve(maze)) - 1


def test_analyzer_accepts_default_pac_man_board(tmp_path: Path) -> None:
    """Check maze_analyzer accepts default mode as Pac-Man usable."""
    maze = _build_maze(perfect=False, seed=42)
    output_file = tmp_path / "maze.txt"
    _write_output(maze, output_file)

    report = maze_analyzer.analyze(
        maze_analyzer.Maze.from_file(str(output_file))
    )
    verdict = maze_analyzer.verdict(report, min_loops=2, max_dead_ends=2)

    assert not report.incoherent
    assert report.disconnected_corridors == 0
    assert report.unreachable_key_cells == ()
    assert report.loops >= 2
    assert report.dead_ends[0] <= 2
    assert verdict.startswith("Pac-Man-USABLE")


def test_analyzer_identifies_perfect_mode(tmp_path: Path) -> None:
    """Check maze_analyzer reports PERFECT=True output as a perfect maze."""
    maze = _build_maze(perfect=True, seed=42)
    output_file = tmp_path / "maze.txt"
    _write_output(maze, output_file)

    report = maze_analyzer.analyze(
        maze_analyzer.Maze.from_file(str(output_file))
    )
    verdict = maze_analyzer.verdict(report, min_loops=2, max_dead_ends=2)

    assert not report.incoherent
    assert report.disconnected_corridors == 0
    assert report.loops == 0
    assert verdict.startswith("PERFECT maze")
