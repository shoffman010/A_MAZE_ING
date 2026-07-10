from mazegen import Maze, MazeGenerator, MazeSolver, Position

maze = Maze(20, 20, "42", Position(0, 0), Position(19, 19))
MazeGenerator(seed=42).generate(maze, perfect=True)

path = MazeSolver().solve(maze)
print(len(path))
