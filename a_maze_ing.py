from maze import Maze
from renderer import Renderer


maze = Maze(10, 15)

renderer = Renderer()
renderer.render(maze)