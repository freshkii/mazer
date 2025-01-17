from mazegenerator import MazeGenerator
from maze import Maze

def main() -> None:
    width, height = 20, 20
    mg = MazeGenerator(width, height)
    grid, start, finish = mg.generate()
    m = Maze(grid, start, finish)
    m.print()

if __name__ == "__main__":
    main()