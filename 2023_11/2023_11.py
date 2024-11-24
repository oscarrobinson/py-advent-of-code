import sys
from common.utils import run
from common.grid import Point, grid_from_lines, min_distance


def is_galaxy(loc: str) -> bool:
    return loc == "#"


class Universe:
    def __init__(self, lines: list[str]):
        self.grid = grid_from_lines(lines)

    def get_expanded_col_indicies(self) -> list[int]:
        indices = []
        for i, col in enumerate(self.grid.val_cols()):
            if all([not is_galaxy(loc) for loc in col]):
                indices.append(i)
        return indices

    def get_expanded_row_indicies(self) -> list[int]:
        indices = []
        for i, row in enumerate(self.grid.val_rows()):
            if all([not is_galaxy(loc) for loc in row]):
                indices.append(i)
        return indices

    def galaxy_locations(self) -> list[Point]:
        points = []
        for cell in self.grid:
            if is_galaxy(cell.val):
                points.append(cell.point)
        return points

    def sum_distances(self, expansion_fac: int) -> int:
        total = 0
        galaxies = self.galaxy_locations()
        expanded_rows = self.get_expanded_row_indicies()
        expanded_cols = self.get_expanded_col_indicies()

        for a_gal in galaxies:
            for b_gal in galaxies:
                min_row = min([a_gal.y, b_gal.y])
                max_row = max([a_gal.y, b_gal.y])
                min_col = min([a_gal.x, b_gal.x])
                max_col = max([a_gal.x, b_gal.x])

                crosses_expanded_rows = [r for r in expanded_rows if r in range(min_row, max_row)]
                crosses_expanded_cols = [c for c in expanded_cols if c in range(min_col, max_col)]

                # as e.g if expanding by factor of 2, that's one additional column
                # expanding by factor of 100, 99 additional columns etc
                num_additional = expansion_fac - 1

                extra_distance = (len(crosses_expanded_cols) * num_additional) + (
                    len(crosses_expanded_rows) * num_additional
                )

                total += min_distance(a_gal, b_gal)
                total += extra_distance
        # div 2 because we considered each pair twice, once in each direction
        return int(total / 2)

    def expand(self):
        self.expand_vert()
        self.expand_horz()

    def __str__(self):
        return str(self.grid)


def test_universe_sum_distances():
    with open("./2023_11/test_input.txt") as file:
        universe = Universe(list(file))

    assert universe.sum_distances(2) == 374
    assert universe.sum_distances(10) == 1030
    assert universe.sum_distances(100) == 8410


def solution_2023_11_A(filename: str) -> int:
    with open(filename) as file:
        lines = list(file)
        universe = Universe(lines)

    return universe.sum_distances(2)


def solution_2023_11_B(filename: str) -> int:
    with open(filename) as file:
        lines = list(file)
        universe = Universe(lines)

    return universe.sum_distances(1000000)


def test_solution_2023_11_A():
    assert solution_2023_11_A("./2023_11/test_input.txt") == 374  # Replace with expected output for the test case


def test_final_solution_2023_11_A():
    assert solution_2023_11_A("./2023_11/input.txt") == 9445168  # Replace with solution when known


def test_solution_2023_11_B():
    assert solution_2023_11_B("./2023_11/test_input.txt") == 82000210  # Replace with expected output for the test case


def test_final_solution_2023_11_B():
    assert solution_2023_11_B("./2023_11/input.txt") == 742305960572  # Replace with solution when known


if __name__ == "__main__":
    run("2023_11", sys.argv[1], solution_2023_11_A, solution_2023_11_B)
