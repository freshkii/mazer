from random import randint
from config import WALL, EMPTY

class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def generate(self) -> list[list[int]]:
        # on crée une grille vide
        grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        start, finish = (0, 0), (self.width - 1, self.height - 1)

        # On génére les murs
        for y in range(self.height):
            for _ in range(randint(2 * self.width // 3, self.width - 1)):
                x = randint(0, self.width - 1)
                if (x, y) not in [start, finish]:
                    grid[y][x] = WALL

        # on vérifie que l'entrée et la sortie sont vides
        grid[start[1]][start[0]] = EMPTY
        grid[finish[1]][finish[0]] = EMPTY

        return grid, start, finish