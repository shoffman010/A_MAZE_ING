from maze import Maze
from renderer import Renderer


maze = Maze(5, 8)

renderer = Renderer()
renderer.render(maze)