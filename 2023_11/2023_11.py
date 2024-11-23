import sys
from common.utils import run
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x},{self.y})"


def min_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


@dataclass
class Cell:
    point: Point
    val: str

    def __str__(self):
        return self.val


class Grid:
    def __init__(self, vals: list[list[str]]):
        # copy so we don't end up with a ref to some other list
        self.vals = list([list(row) for row in vals])

    def width(self):
        return len(self.vals[0]) if len(self.vals) > 0 else 0

    def height(self):
        return len(self.vals)

    def val_rows(self):
        return list([list(row) for row in self.vals])

    def val_cols(self):
        grid_width = self.width()
        if grid_width > 0:
            cols = []
            for i in range(0, grid_width):
                cols.append([row[i] for row in self.val_rows()])
            return cols
        else:
            return []

    def __iter__(self):
        for y, row in enumerate(self.vals):
            for x, val in enumerate(row):
                yield Cell(Point(x, y), val)

    def __str__(self):
        return "\n".join(["".join(row) for row in self.vals])


def grid_from_lines(lines: list[str]) -> Grid:
    vals = []
    for line in lines:
        vals.append(list(line.strip()))
    return Grid(vals)


def test_grid_not_ref_to_passed_list():
    original_list = [["a", "b"], ["c", "d"]]
    grid = Grid(original_list)
    original_list[0][0] = "x"
    assert original_list[0][0] == "x"
    assert grid.val_rows()[0][0] == "a"


def test_grid_width():
    assert grid_from_lines(["ab", "cd"]).width() == 2


def test_empty_grid_width():
    assert grid_from_lines([]).width() == 0


def test_grid_iterator():
    raw_grid = ["ab", "cd"]
    grid = grid_from_lines(raw_grid)
    assert list(grid) == [
        Cell(Point(0, 0), "a"),
        Cell(Point(1, 0), "b"),
        Cell(Point(0, 1), "c"),
        Cell(Point(1, 1), "d"),
    ]


def test_grid_val_cols():
    raw_grid = ["ab", "cd"]
    grid = grid_from_lines(raw_grid)
    assert grid.val_cols() == [["a", "c"], ["b", "d"]]


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
