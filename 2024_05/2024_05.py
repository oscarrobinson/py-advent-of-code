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


def is_valid(update: list[int], required_afters: dict[int, set[int]]) -> bool:
    valid = True
    for i in range(0, len(update)):
        val_at_i = update[i]
        if any([val in required_afters[val_at_i] for val in list_before(i, update)]):
            valid = False
            break
    return valid


def get_required_afters(constraints: list[(int, int)]) -> dict[int, set[int]]:
    required_afters = defaultdict(set)
    for before, after in constraints:
        required_afters[before].add(after)
    return required_afters


def solution_2024_05_A(filename: str) -> int:
    raw_constraints, updates = parse_input(filename)
    required_afters = get_required_afters(raw_constraints)
    result = 0
    for update in updates:
        if is_valid(update, required_afters):
            result += get_middle(update)
    return result


def solution_2024_05_B(filename: str) -> int:
    raw_constraints, updates = parse_input(filename)

    required_afters = get_required_afters(raw_constraints)

    invalids = []

    for update in updates:
        if not is_valid(update, required_afters):
            invalids.append(update)

    result = 0

    for update in invalids:
        while not is_valid(update, required_afters):
            for i in range(0, len(update)):
                required_after_i = required_afters[update[i]]
                # Swap value at i with value at j if value at j should be after i
                for j in range(0, i):
                    if update[j] in required_after_i:
                        temp = update[i]
                        update[i] = update[j]
                        update[j] = temp
                        break
        result += get_middle(update)

    return result


def test_solution_2024_05_A():
    assert solution_2024_05_A("./2024_05/test_input.txt") == 143  # Replace with expected output for the test case


def test_final_solution_2024_05_A():
    assert solution_2024_05_A("./2024_05/input.txt") == 4281  # Replace with solution when known


def test_solution_2024_05_B():
    assert solution_2024_05_B("./2024_05/test_input.txt") == 123  # Replace with expected output for the test case


def test_final_solution_2024_05_B():
    assert solution_2024_05_B("./2024_05/input.txt") == 5466  # Replace with solution when known


if __name__ == "__main__":
    run("2024_05", sys.argv[1], solution_2024_05_A, solution_2024_05_B)
