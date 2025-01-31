from maze_generator import MazeGenerator
from maze import Maze
from random import randint

def main() -> None:
<<<<<<< Updated upstream
    width, height = randint(20, 30), randint(20, 30)
    mg = MazeGenerator(width, height)
    grid, start, finish = mg.generate()
    m = Maze(grid, start, finish)
    print(m)
=======
    width, height = 20, 20
    maze_generator = MazeGenerator(width, height)
    grid, start, finish = maze_generator.generate()
    maze = Maze(grid, start, finish)
    print(maze)
>>>>>>> Stashed changes

if __name__ == "__main__":
    main()