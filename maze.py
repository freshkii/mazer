from config import Coord, EMPTY, WALL


class Maze:
    def __init__(self, grid: list[list[int]], start: Coord, finish: Coord):
        self.grid = grid
        self.start = start
        self.finish = finish
        self.width = len(grid[0])  # Largeure du labyrinthe
        self.height = len(grid)    # Longueure du labyrinthe

    def is_valid_coord(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == EMPTY

    def print(self) -> None:
        # Affichage du labyrinthe
        for row in self.grid:
            print(''.join(['██' if cell == WALL else '  ' for cell in row]))