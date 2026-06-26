*This project has been created as part of the 42 curriculum by stehoffm, archowdh.*

# A-Maze-ing

## Description

A-Maze-ing is a Python 3 maze generator for the 42 curriculum. It reads a plain
text configuration file, generates a maze, displays it in the terminal, and can
save the result in the hexadecimal wall format required by the subject.

The maze is built as a grid of cells. Each cell stores four wall flags: north,
east, south, and west. A protected central pattern is kept closed so the visual
rendering contains a visible `42`. The program can generate either a perfect
maze, with exactly one route between cells, or an imperfect maze with a limited
number of extra passages.

The project includes:

- `a_maze_ing.py`: main entry point.
- `config.py`: configuration parser and validator.
- `maze.py`, `cell.py`, `position.py`, `direction.py`: maze data model.
- `maze_generator.py`: reusable maze generation logic.
- `maze_solver.py`: shortest-path solver.
- `maze_writer.py`: output-file writer.
- `renderer.py`: terminal renderer.
- `menu_ui.py`: interactive menu.

## Instructions

### Requirements

- Python 3.10 or later.
- `pip`, used by the `Makefile` to install linting tools.

Install the development tools:

```sh
make install
```

Run the project with the default configuration:

```sh
make run
```

Or run it directly with a chosen configuration file:

```sh
python3 a_maze_ing.py config.txt
```

Run the debugger:

```sh
make debug
```

Run lint and type checks:

```sh
make lint
```

Remove generated cache files:

```sh
make clean
```

### Interactive Menu

After startup, the program opens a terminal menu with these actions:

- Generate a new maze.
- Show the shortest solution path.
- Hide the solution path.
- Change wall, path, and pattern colours.
- Save the maze to the configured output file.
- Exit.

## Configuration File

The configuration file contains one `KEY=VALUE` pair per line. Empty lines and
lines beginning with `#` are ignored.

Example:

```txt
# Default A-Maze-ing configuration
WIDTH=20
HEIGHT=20
ENTRY=1,1
EXIT=8,5
OUTPUT_FILE=maze.txt
PERFECT=False
PATTERN=42
SEED=
WALL_COLOR=DEFAULT
PATH_COLOR=RED
PATTERN_COLOR=CYAN
```

Mandatory keys:

| Key | Format | Description |
| --- | --- | --- |
| `WIDTH` | Positive integer | Maze width in cells. |
| `HEIGHT` | Positive integer | Maze height in cells. |
| `ENTRY` | `x,y` | Entry cell coordinates. |
| `EXIT` | `x,y` | Exit cell coordinates. |
| `OUTPUT_FILE` | Path | Destination file for the serialized maze. |
| `PERFECT` | `True` or `False` | Whether the generated maze must have only one path. |

Optional keys:

| Key | Format | Default | Description |
| --- | --- | --- | --- |
| `PATTERN` | Pattern name | `42` | Protected pattern drawn in the maze. The required subject pattern is `42`. |
| `SEED` | Integer or empty | Empty | When set, the same seed recreates the same maze choices. |
| `WALL_COLOR` | Colour name | `DEFAULT` | Terminal colour used for maze walls. |
| `PATH_COLOR` | Colour name | `RED` | Terminal colour used for the solution path. |
| `PATTERN_COLOR` | Colour name | `CYAN` | Terminal colour used for the protected pattern. |

Supported colour names are `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`,
`MAGENTA`, `CYAN`, `WHITE`, and `DEFAULT`.

Coordinates are written as `x,y` in the config file. Internally, the code stores
positions as `row,column`, so `ENTRY=1,4` becomes row `4`, column `1`.

## Output File Format

The output file stores the maze as one hexadecimal digit per cell. Each digit
encodes the closed walls of that cell:

| Bit | Direction | Value |
| --- | --- | --- |
| 0 | North | `1` |
| 1 | East | `2` |
| 2 | South | `4` |
| 3 | West | `8` |

A closed wall sets its bit to `1`; an open wall leaves it as `0`. For example,
`3` means north and east are closed, while `A` means east and west are closed.

Cells are written row by row. After an empty line, the file contains:

1. Entry coordinates.
2. Exit coordinates.
3. The shortest valid path from entry to exit, using `N`, `E`, `S`, and `W`.

## Generation Algorithm

The chosen generation algorithm is recursive backtracking, implemented as a
randomized depth-first search in `MazeGenerator`.

The generator starts at the entry cell, marks it visited, shuffles the available
unvisited neighbours, opens a wall to one neighbour, and recursively continues
from that neighbour. This creates a spanning tree over all reachable unlocked
cells.

Reasons for choosing recursive backtracking:

- It naturally creates perfect mazes when no extra passages are added.
- It is simple to explain during evaluation.
- It works directly with the project's cell and wall model.
- It supports reproducibility by using a local `random.Random(seed)` instance.
- It is easy to adapt for the required protected `42` cells by excluding locked
  cells from the neighbour list.

When `PERFECT=False`, the generator adds a controlled number of extra passages
after the first pass. These additions make the maze imperfect while avoiding
oversized open rooms such as `3x3`, `2x4`, or `4x2` empty rectangles.

## Reusable Generator

The reusable generation logic lives in `maze_generator.py` and is centered on
the `MazeGenerator` class. It can be imported by another Python project together
with the maze model and solver.

Basic use:

```python
from maze import Maze
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from position import Position

maze = Maze(
    rows=20,
    cols=20,
    pattern_name="42",
    entry=Position(0, 0),
    exit=Position(19, 19),
)

generator = MazeGenerator(seed=42)
generator.generate(maze, perfect=True)

solver = MazeSolver()
solution = solver.solve(maze)
```

Using custom size and seed:

```python
maze = Maze(30, 40, "42", entry=Position(1, 1), exit=Position(28, 38))
generator = MazeGenerator(seed=12345)
generator.generate(maze, perfect=False)
```

Accessing the generated structure:

```python
cell = maze.get_cell(Position(0, 0))

print(cell.north, cell.east, cell.south, cell.west)
print(cell.hex_value)
```

Retrieving a solution:

```python
path = MazeSolver().solve(maze)
for position in path:
    print(position.row, position.col)
```

The generator mutates the `Maze` object in place. The maze structure does not
need to match the serialized output format; `MazeWriter` converts it when saving.

## Visual Representation

The project uses terminal rendering. Walls are displayed as block characters,
open cells as spaces, the entry as `EN`, the exit as `EX`, and the optional
solution path as coloured dots. The protected pattern is drawn with closed cells
and can use a separate colour.

## Team and Project Management

This repository was developed as a team project by `stehoffm` and `archowdh`.

Role:

- `stehoffm`: terminal rendering and canvas creation, complete configuration
  parsing, protected pattern implementation, locking cells that belong to the
  pattern, imperfect maze generation, `Makefile`, docstrings, and README
  documentation.
- `archowdh`: grid initialization, perfect maze generation with DFS/recursive
  backtracking, shortest-path solver, and interactive menu options.
- Shared work: the first version of the `Cell` class, which became the starting
  point for the maze data model.

Initial planning:

- Read the subject and identify mandatory files, commands, and formats.
- Start with a small `Cell` model so the rest of the project had a common data
  structure.
- Add grid initialization and recursive backtracking generation.
- Add the protected `42` pattern and make sure its cells stay locked.
- Add solving, rendering, menu interaction, and output serialization.
- Add config validation, imperfect generation, linting support, docstrings, and
  README updates.

How the planning evolved:

- The reusable API became clearer after separating `Maze`, `MazeGenerator`, and
  `MazeSolver`.
- Optional display colours were added through config and the menu.
- Reproducible seed support was kept separate from global randomness by using a
  dedicated random generator instance.
- The work split became more focused as the project grew: `archowdh` worked
  mainly on generation, solving, grid setup, and menu flow, while `stehoffm`
  worked mainly on parsing, rendering, pattern handling, imperfect mazes, and
  project polish.

What worked well:

- Keeping cells responsible for their own hexadecimal wall encoding.
- Keeping parsing and validation in `config.py`.
- Using a separate solver to verify and display the shortest path.

What could be improved:

- Add automated tests for config parsing, wall coherence, seed reproducibility,
  and saved output.
- Add a packaged `mazegen-*` build artifact for the reusable module.
- Keep the mandatory `42` path as the default and document any alternate pattern
  support as optional behaviour.

Tools used:

- Python 3.10+.
- `make` for common commands.
- `flake8` for style checks.
- `mypy` for type checks.
- Git for version control.

## Resources

Classic references:

- 42 A-Maze-ing subject, version 2.0.
- Python documentation: <https://docs.python.org/3/>
- `random.Random` documentation: <https://docs.python.org/3/library/random.html>
- `dataclasses` documentation: <https://docs.python.org/3/library/dataclasses.html>
- `collections.deque` documentation: <https://docs.python.org/3/library/collections.html#collections.deque>
- Jamis Buck, "Maze Generation: Recursive Backtracking":
  <https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking>
- Wikipedia, "Maze generation algorithm":
  <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
- Wikipedia, "Depth-first search":
  <https://en.wikipedia.org/wiki/Depth-first_search>
- Wikipedia, "Breadth-first search":
  <https://en.wikipedia.org/wiki/Breadth-first_search>

AI use:

- AI was used as a support tool for reviewing the subject requirements,
  organizing the implementation checklist, improving documentation wording, and
  checking for likely edge cases.
- AI suggestions were reviewed against the code and subject before being kept.
- The project owner remains responsible for understanding, testing, and defending
  the implementation.
