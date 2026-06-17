from maze import Maze
class Renderer:
    def render(self, maze: Maze) -> None:
        for row in maze.grid:
            for _ in row:
                print("#", end=" ")
            print()
        
        
        print()
        print("==================Hex Value =================")
        for row in maze.grid:
            line = "".join(cell.hex_value for cell in row)
            print(line)

