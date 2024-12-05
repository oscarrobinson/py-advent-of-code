import sys
import math
from common.utils import run
from collections import defaultdict


def get_middle(list: int) -> int:
    return list[math.floor(len(list) / 2)]


def parse_input(filename) -> (list[(int, int)], list[list[int]]):
    constraints = []
    updates = []
    with open(filename) as lines:
        for line in lines:
            if "|" in line:
                x, y = line.split("|")
                constraints.append((int(x.strip()), int(y.strip())))
            elif line != "\n":
                updates.append([int(z.strip()) for z in line.split(",") if z != "\n"])
    return (constraints, updates)


def list_before(i: int, list: list[int]) -> list[int]:
    return list[0:i]


def list_after(i: int, list: list[int]) -> list[int]:
    return list[i + 1 :]


def solution_2024_05_A(filename: str) -> int:
    constraints, updates = parse_input(filename)
    before_constraints = defaultdict(set)
    after_constraints = defaultdict(set)

    for before, after in constraints:
        before_constraints[before].add(after)
        after_constraints[after].add(before)

    result = 0

    for update in updates:
        valid = True
        for i in range(0, len(update)):
            must_be_after = after_constraints[update[i]]
            must_be_before = before_constraints[update[i]]
            before = set(list_before(i, update))
            after = set(list_after(i, update))
            before_valid = len(must_be_after.intersection(after)) == 0
            after_valid = len(must_be_before.intersection(before)) == 0
            if not (before_valid and after_valid):
                valid = False
                break
        if valid:
            result += get_middle(update)

    return result


def solution_2024_05_B(filename: str) -> int:
    return 0


def test_solution_2024_05_A():
    assert solution_2024_05_A("./2024_05/test_input.txt") == 143  # Replace with expected output for the test case


# def test_final_solution_2024_05_A():
#    assert solution_2024_05_A('./2024_05/input.txt') == 0 # Replace with solution when known


def test_solution_2024_05_B():
    assert solution_2024_05_B("./2024_05/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_05_B():
#    assert solution_2024_05_B('./2024_05/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_05", sys.argv[1], solution_2024_05_A, solution_2024_05_B)
