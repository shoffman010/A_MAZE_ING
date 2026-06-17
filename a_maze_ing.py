from maze import Maze
from renderer import Renderer


maze = Maze(5, 8)

renderer = Renderer()
renderer.render(maze)

# Print the Grid, height x width

# def initialize_maze(row: int, col: int):
#     #row = 0 and col = 0 = north + west Outer boarder
#     #row = 0 and col = max north + east Outer boarder
#     #row = max col = 0 = south + west Outer boarder
#     #row = max col = max = south + east Outer boarder
#     #all the above cannot be touched, or changed. could be tuples or somehow else not accessible
#     #Then initialize to all true for the whole inner grid, later we remove the walls when we use DFS
    