from sys import exit
from random import randint, shuffle, uniform
from math import sqrt, cos, sin, radians

BOLD = "\033[1m{}\033[0m"
RED = "\033[0;31m{}\033[0m"
GREEN = "\033[0;32m{}\033[0m"
BLUE = "\033[0;34m{}\033[0m"
CYAN = "\033[0;36m{}\033[0m"

symbols = {
    '#': "██",
    's': GREEN.format("██"),
    'S': BLUE.format("██"),
    'F': RED.format("██"),
    ' ': "  "
}

patterns = ((-1, 0), (1, 0), (0, -1), (0, 1))


def print_error(text):
    print(RED.format("error: "+text))


class MazeManager():
    def __init__(self):
        pass

    def generate_walls_from_center(self, maze, center, radius,
                                   num_walls, noise_level):
        """
        Generate walls in the labyrinth

        :param maze: Maze class instance
        :param center: coordinates of the maze center
        :param radius: radius from which the walls will be generated
        :param num_walls: number of walls to generate
        :param noise_level: noise to add
        """

        for i in range(num_walls):
            angle = radians(i * (360 / num_walls))
            x = int(center[0] + radius * cos(angle) + uniform(-noise_level,
                                                              noise_level))
            y = int(center[1] + radius * sin(angle) + uniform(-noise_level,
                                                              noise_level))

            if maze.cell_valid((x, y)):
                maze.grid[y][x] = '#'

    def generate_maze(self, width: int, height: int):
        """
        :param width: width of the maze grid
        :param height: height of the maze grid
        Returns a Maze object with walls, start and finish of the specified
        dimensions
        """
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

    def generate_maze_with_cosinus(self, width: int, height: int):
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        start, finish = (0, 0), (width-1, height-1)
        center = (width // 2, height // 2)
        radius = min(width, height) // 3
        num_walls = width*height // 3
        noise_level = 5

        m = Maze(grid)
        self.generate_walls_from_center(m, center, radius,
                                        num_walls, noise_level)
        m.set_start_finish(start, finish)
        return m


class Maze:
    def __init__(self, grid: list[list[int]]):
        self.grid = grid[:]
        self.height = len(grid)
        self.width = len(grid[0])
        self.start, self.finish = None, None

    def set_start_finish(self, start, finish):
        self.grid[start[1]][start[0]] = 'S'
        self.grid[finish[1]][finish[0]] = 'F'
        self.start = start
        self.finish = finish

    def print(self, solution=False):
        for row in self.grid:
            for cell in row:
                if cell == 's' and not solution:
                    print(symbols[' '], end='')
                else:
                    print(symbols[cell], end='')
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

    def solve(self) -> bool:
        """
        Returns True if a solution exists, False otherwise
        """
        from collections import deque
        queue = deque([self.start])
        visited = set()
        parent = {self.start: None}

        while queue:
            current = queue.popleft()
            if current == self.finish:
                while current != self.start:
                    self.grid[current[1]][current[0]] = 's'
                    current = parent[current]
                self.grid[current[1]][current[0]] = 's'
                return True

            for neighbor in self.get_patterns(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        return False


def get_input(input_func, retry_text=None):
    while True:
        try:
            value = input_func()

            if value:
                return value

            if retry_text:
                print(BLUE.format(retry_text))

        except KeyboardInterrupt:
            print("\nInterruption")
            exit(0)


def input_user_maze(manager: MazeManager):
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
    title = BOLD.format("Maze solver")
    print(GREEN.format("┌─────────────┐"))
    print(GREEN.format('│'), title,  GREEN.format('│'))
    print(GREEN.format("└─────────────┘"))

    print("by", CYAN.format("atom-man59"), "and", CYAN.format("freshkii"),
          "\n\n")

    manager = MazeManager()

    if input("type anything if you want to pass in a maze else a maze will be randomly generated: "):
        maze = get_input(lambda: input_user_maze(manager))
        start, finish = map(lambda x: tuple(map(int, x.split(","))),
                            get_input(lambda: input("enter start and finish cell (xs,ys xf,yf): "))
                            .split())
        maze.set_start_finish(start, finish)
        maze.print()
    else:
        maze = manager.generate_maze_with_cosinus(20, 20)
        maze.print()

    if maze.solve():
        print("\nSolution found:")
        maze.print(solution=True)
    else:
        print("\nNo solution found.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterruption")