from pathlib import Path

from setuptools import setup


setup(
    name="mazegen",
    version="1.0.0",
    description="Reusable maze generation module for A-Maze-ing",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    py_modules=[
        "mazegen",
        "maze_generator",
        "maze_solver",
        "maze_writer",
        "maze",
        "cell",
        "position",
        "direction",
    ],
    python_requires=">=3.10",
)
