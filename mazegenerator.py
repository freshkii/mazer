from config import WALL, EMPTY, Coord
from random import shuffle

move_patterns = ((0,-1), (0,1), (-1,0), (1,0))


class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def is_valid_case(self, case: Coord) -> bool:
        return 0 <= case[1] <= self.height-1 and 0 <= case[0] <= self.width-1

    def generate(self) -> list[list[int]]:
        grid = [[WALL for _ in range(self.width)] for _ in range(self.height)]
        start, finish = (0, 0), (self.width - 1, self.height - 1)

        def move(current_case, last_case=None):
            if current_case == finish:
                grid[finish[1]][finish[0]] = EMPTY
                return

            cases = []
            for pattern in move_patterns:
                case = (pattern[0] + current_case[0],
                        pattern[1] + current_case[1])
                if self.is_valid_case(case):
                    if last_case and case != last_case:
                        cases.append(case)
                    elif not last_case:
                        cases.append(case)

            ok = True

            for c in cases:
                if self.is_valid_case(c) and grid[c[1]][c[0]] == EMPTY:
                    ok = False
                    break
            if not ok:
                return

            grid[current_case[1]][current_case[0]] = EMPTY
            
            shuffle(cases)

            for case in cases:
                if self.is_valid_case(case):
                    move(case, current_case)


        move(start)

        grid[start[1]][start[0]] = EMPTY

        return grid, start, finish
