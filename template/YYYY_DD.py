import sys
from common.utils import run


def solution_YYYY_DD_A(filename: str) -> int:
    return 0


def solution_YYYY_DD_B(filename: str) -> int:
    return 0


def test_solution_YYYY_DD_A():
    assert solution_YYYY_DD_A("./YYYY_DD/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_YYYY_DD_A():
#    assert solution_YYYY_DD_A('./YYYY_DD/input.txt') == 0 # Replace with solution when known


def test_solution_YYYY_DD_B():
    assert solution_YYYY_DD_B("./YYYY_DD/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_YYYY_DD_B():
#    assert solution_YYYY_DD_B('./YYYY_DD/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("YYYY_DD", sys.argv[1], solution_YYYY_DD_A, solution_YYYY_DD_B)
