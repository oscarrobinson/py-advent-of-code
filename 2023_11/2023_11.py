import sys
from common.utils import run
from common.grid import Grid, Point, grid_from_lines, min_distance


def is_galaxy(loc: str) -> bool:
    return loc == "#"


class Universe:
    def __init__(self, lines: list[str]):
        self.grid = grid_from_lines(lines)

    def expand_vert(self):
        new_grid = []

        for row in self.grid.val_rows():
            if all([not is_galaxy(loc) for loc in row]):
                new_grid.append(row)
                new_grid.append(row)
            else:
                new_grid.append(row)

        self.grid = Grid(new_grid)

    def expand_horz(self):
        new_grid = []

        height = self.grid.height()

        for y in range(0, height):
            new_grid.append([])

        for x, col in enumerate(self.grid.val_cols()):
            if all([not is_galaxy(loc) for loc in col]):
                for y in range(0, height):
                    new_grid[y].append(".")
                    new_grid[y].append(".")
            else:
                for y, val in enumerate(col):
                    new_grid[y].append(val)

        self.grid = Grid(new_grid)

    def galaxy_locations(self) -> list[Point]:
        points = []
        for cell in self.grid:
            if is_galaxy(cell.val):
                points.append(cell.point)
        return points

    def sum_shortest_distances(self) -> int:
        total = 0
        galaxies = self.galaxy_locations()

        for galaxy_a in galaxies:
            for galaxy_b in galaxies:
                total += min_distance(galaxy_a, galaxy_b)

        return int(total / 2)

    def expand(self):
        self.expand_vert()
        self.expand_horz()

    def __str__(self):
        return str(self.grid)


def solution_2023_11_A(filename: str) -> int:
    with open(filename) as file:
        lines = list(file)
        universe = Universe(lines)

    universe.expand()

    return universe.sum_shortest_distances()


def solution_2023_11_B(filename: str) -> int:
    return 0


def test_solution_2023_11_A():
    assert solution_2023_11_A("./2023_11/test_input.txt") == 374  # Replace with expected output for the test case


def test_final_solution_2023_11_A():
    assert solution_2023_11_A("./2023_11/input.txt") == 9445168  # Replace with solution when known


def test_solution_2023_11_B():
    assert solution_2023_11_B("./2023_11/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2023_11_B():
#    assert solution_2023_11_B('./2023_11/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2023_11", sys.argv[1], solution_2023_11_A, solution_2023_11_B)
