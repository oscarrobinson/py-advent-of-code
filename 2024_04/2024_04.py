import sys
import re
from common.utils import run
from common.grid import grid_from_lines


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


def solution_2024_04_B(filename: str) -> int:
    return 0


def test_solution_2024_04_A():
    assert solution_2024_04_A("./2024_04/test_input.txt") == 18  # Replace with expected output for the test case


def test_final_solution_2024_04_A():
    assert solution_2024_04_A("./2024_04/input.txt") == 2562  # Replace with solution when known


def test_solution_2024_04_B():
    assert solution_2024_04_B("./2024_04/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_04_B():
#    assert solution_2024_04_B('./2024_04/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_04", sys.argv[1], solution_2024_04_A, solution_2024_04_B)
