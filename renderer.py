from maze import Maze
class Renderer:
    OUT_TOP_LEFT = "╔"
    OUT_TOP_RIGHT = "╗"
    OUT_BOTTOM_LEFT = "╚"
    OUT_BOTTOM_RIGHT = "╝"
    OUT_VERTICAL = "║"
    OUT_HORIZONTAL = "═"

    IN_VERTICAL = "│"
    IN_HORIZONTAL = "─"
    
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

