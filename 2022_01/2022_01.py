import sys
from common.utils import run


def get_total_cals(lines: list[str]) -> list[int]:
    totals = []
    running_total = 0
    for line in lines:
        stripped_line = line.strip()
        if stripped_line != "":
            running_total += int(stripped_line)
        else:
            totals.append(running_total)
            running_total = 0
    totals.append(running_total)
    running_total = 0
    return totals


def solution_2022_01_A(filename: str) -> int:
    with open(filename) as lines:
        return max(get_total_cals(lines))


def solution_2022_01_B(filename: str) -> int:
    with open(filename) as lines:
        return sum(sorted(get_total_cals(lines), reverse=True)[0:3])


def test_solution_2022_01_A():
    assert solution_2022_01_A("./2022_01/test_input.txt") == 24000  # Replace with expected output for the test case


def test_final_solution_2022_01_A():
    assert solution_2022_01_A("./2022_01/input.txt") == 69501  # Replace with solution when known


def test_solution_2022_01_B():
    assert solution_2022_01_B("./2022_01/test_input.txt") == 45000  # Replace with expected output for the test case


def test_final_solution_2022_01_B():
    assert solution_2022_01_B("./2022_01/input.txt") == 202346  # Replace with solution when known


if __name__ == "__main__":
    run("2022_01", sys.argv[1], solution_2022_01_A, solution_2022_01_B)
