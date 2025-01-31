from mazegenerator import MazeGenerator
from maze import Maze
from random import randint

def main() -> None:
    width, height = randint(20, 30), randint(20, 30)
    mg = MazeGenerator(width, height)
    grid, start, finish = mg.generate()
    m = Maze(grid, start, finish)
    print(m)

if __name__ == "__main__":
    main()