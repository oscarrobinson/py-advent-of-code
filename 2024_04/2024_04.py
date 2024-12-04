import sys
import re
from common.utils import run
from common.grid import grid_from_lines
from common.grid import Point, Grid


def solution_2024_04_A(filename: str) -> int:
    with open(filename) as lines:
        wordsearch = grid_from_lines(list(lines))
        row_strs = ["".join(row) for row in wordsearch.val_rows()]
        col_strs = ["".join(col) for col in wordsearch.val_cols()]
        diag_lr_strs = ["".join(diag) for diag in wordsearch.val_lr_diags()]
        diag_rl_strs = ["".join(diag) for diag in wordsearch.val_rl_diags()]
        search_space = row_strs + col_strs + diag_lr_strs + diag_rl_strs
        pattern = r"XMAS"
        occurences = sum([len(re.findall(pattern, search_str)) for search_str in search_space])
        rev_search_space = ["".join(list(reversed(search_str))) for search_str in search_space]
        rev_occurences = sum([len(re.findall(pattern, search_str)) for search_str in rev_search_space])
        return occurences + rev_occurences


def has_x_mas_centered_on(wordsearch: Grid, point: Point) -> bool:
    c = wordsearch.val(point)
    tl = wordsearch.val(Point(point.x - 1, point.y - 1))
    tr = wordsearch.val(Point(point.x + 1, point.y - 1))
    bl = wordsearch.val(Point(point.x - 1, point.y + 1))
    br = wordsearch.val(Point(point.x + 1, point.y + 1))

    if c == "A":
        if (tl == "M" and br == "S") or (tl == "S" and br == "M"):
            if (tr == "M" and bl == "S") or (tr == "S" and bl == "M"):
                return True
    return False


def solution_2024_04_B(filename: str) -> int:
    with open(filename) as lines:
        wordsearch = grid_from_lines(list(lines))
        total = 0
        for x in range(0, wordsearch.width()):
            for y in range(0, wordsearch.height()):
                if has_x_mas_centered_on(wordsearch, Point(x, y)):
                    total += 1
        return total


def test_solution_2024_04_A():
    assert solution_2024_04_A("./2024_04/test_input.txt") == 18  # Replace with expected output for the test case


def test_final_solution_2024_04_A():
    assert solution_2024_04_A("./2024_04/input.txt") == 2562  # Replace with solution when known


def test_solution_2024_04_B():
    assert solution_2024_04_B("./2024_04/test_input.txt") == 9  # Replace with expected output for the test case


# def test_final_solution_2024_04_B():
#    assert solution_2024_04_B('./2024_04/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_04", sys.argv[1], solution_2024_04_A, solution_2024_04_B)
