from sys import exit
from random import randint, shuffle, uniform
from math import sqrt, cos, sin, radians
from time import sleep

bold = "\033[1m{}\033[0m"
red = "\033[0;31m{}\033[0m"
green = "\033[0;32m{}\033[0m"
blue = "\033[0;34m{}\033[0m"
cyan = "\033[0;36m{}\033[0m"

patterns = ((-1, 0), (1, 0), (0, -1), (0, 1))

def print_error(text):
    print(red.format("error: "+text))

class Maze:
    def __init__(self, grid: list[list[int]]):
        self.grid = grid[:]
        self.height = len(grid)
        self.width = len(grid[0])
        self.start, self.finish = None, None

    def generate_maze(width: int, height: int):
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        start, finish = (0, 0), (width-1, height-1)
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        m = Maze(grid)
        case = start
        forbidden_cells = [start]
        path = []
        diago = width**2+height**2
        while case != finish:
            cells = m.get_patterns(case)
            for c in cells:
                for fc in forbidden_cells:
                    if fc in cells:
                        cells.remove(fc)
                for pc in path:
                    if pc in cells:
                        cells.remove(pc)
            if len(cells) == 0:
                case = start
                forbidden_cells = [start]
                path = [start]
                continue
            proba = []
            for c in cells:
                dist = sqrt((c[0] - finish[0])**2+(c[1] - finish[1])**2)+1
                proba += [c for _ in range(int(diago/dist)**2)]
            shuffle(proba)
            forbidden_cells += cells
            path.append(proba[0])
            case = proba[0]

        m.start, m.finish = start, finish
        m.grid[start[1]][start[0]] = 'S'
        m.grid[finish[1]][finish[0]] = 'F'
        path.append(start)
        path.append(finish)

        for y in range(height):
            for _ in range(randint(2*width//3, width-1)):
                x = randint(0, width-1)
                if (x, y) not in path:
                    m.grid[y][x] = '#'

        return m

    def set_start_finish(self, start, finish):
        self.grid[start[1]][start[0]] = 'S'
        self.grid[finish[1]][finish[0]] = 'F'
        self.start = start
        self.finish = finish

    def print(self, solution=False):
        for row in self.grid:
            for cell in row:
                if solution:
                    if cell == '#': print("██",end='')
                    elif cell == 's': print(green.format("██"),end='')
                    elif cell == 'S': print(blue.format("██"),end='')
                    elif cell == 'F': print(red.format("██"),end='')
                    else: print("  ", end='')
                else:
                    if cell == '#': print("██",end='')
                    elif cell == 'S': print(blue.format("██"), end='')
                    elif cell == 'F': print(red.format("██"),end='')
                    else: print("  ", end='')
            print()

    def get_cell(self, cell: tuple[int]) -> str | int:
        return self.grid[cell[1]][cell[0]]

    def cell_valid(self, cell: tuple[int]) -> bool:
        return 0 <= cell[0] < self.width and 0 <= cell[1] < self.height

    def get_patterns(self, cell: tuple[int]) -> list[tuple[int]]:
        output = []
        for pattern in patterns:
            cords = cell[0] + pattern[0], cell[1] + pattern[1]
            if (self.cell_valid(cords) and self.get_cell(cords) != '#'):
                output.append(cords)
        return output

    def solve(self):
        from collections import deque
        queue = deque([self.start])
        visited = set()
        parent = {self.start: None}

        while queue:
            current = queue.popleft()
            if current == self.finish:
                path = []
                while current:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                for cell in path:
                    self.grid[cell[1]][cell[0]] = 's'
                return path

            for neighbor in self.get_patterns(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return None

def generate_walls_from_center(maze, center, radius, num_walls, noise_level):
    """
    Génère des murs dans le labyrinthe à partir du centre en utilisant les fonctions cosinus et sinus avec du bruit.

    :param maze: L'instance de la classe Maze.
    :param center: Les coordonnées du centre du labyrinthe (x, y).
    :param radius: Le rayon à partir duquel les murs seront générés.
    :param num_walls: Le nombre de murs à générer.
    :param noise_level: Le niveau de bruit à ajouter aux positions des murs.
    """
    for i in range(num_walls):
        angle = radians(i * (360 / num_walls))
        x = int(center[0] + radius * cos(angle) + uniform(-noise_level, noise_level))
        y = int(center[1] + radius * sin(angle) + uniform(-noise_level, noise_level))

        if maze.cell_valid((x, y)):
            maze.grid[y][x] = '#'

def generate_maze_with_cosinus(width: int, height: int):
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    start, finish = (0, 0), (width-1, height-1)
    center = (width // 2, height // 2)
    radius = min(width, height) // 3
    num_walls = 90  # Nombre de murs à générer
    noise_level = 5  # Niveau de bruit à ajouter aux positions des murs

    m = Maze(grid)
    generate_walls_from_center(m, center, radius, num_walls, noise_level)

    m.set_start_finish(start, finish)
    return m

def get_input(input_func, retry_text=None):
    while True:
        try:
            value = input_func()

            if value:
                return value

            if retry_text:
                print(blue.format(retry_text))

        except KeyboardInterrupt:
            print("\nInterruption")
            exit(0)

def input_user_maze():
    try:
        height, width = map(int,
                            input("enter maze dimensions (height width): ")
                            .split())
    except ValueError:
        print_error("incorrect dimensions")
        return
    grid = []
    print("enter maze grid:")
    for _ in range(height):
        line = input()

        if len(line) > width:
            print(line)
            print_error("line too long")
            return

        line += (width-len(line))*' '
        grid.append(list(line))

    return Maze(grid)

def main():
    title = bold.format("Maze solver")
    print(green.format("┌─────────────┐"))
    print(green.format('│'), title,  green.format('│'))
    print(green.format("└─────────────┘"))

    print("by", cyan.format("atom-man59"), "and", cyan.format("freshkii"),
          "\n\n")

    if input("type anything if you want to pass in a maze else a maze will be randomly generated: "):
        maze = get_input(input_user_maze)
        start, finish = map(lambda x: tuple(map(int, x.split(","))),
                            get_input(lambda: input("enter start and finish cell (xs,ys xf,yf): "))
                            .split())
        maze.set_start_finish(start, finish)
        maze.print()
    else:
        maze = generate_maze_with_cosinus(20, 20)
        maze.print()

    solution = maze.solve()
    if solution:
        print("\nSolution found:")
        maze.print(solution=True)
    else:
        print("\nNo solution found.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterruption")
