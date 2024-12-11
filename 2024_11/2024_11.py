import sys
from common.utils import run
from functools import cache


@cache
def get_num_stones(stone: int, after_blinks: int):
    if after_blinks == 0:
        return 1
    elif stone == 0:
        return get_num_stones(1, after_blinks - 1)
    elif len(str(stone)) % 2 == 0:
        stone = str(stone)
        halfway = int(len(stone) / 2)
        half_num_1 = int(stone[0:halfway])
        half_num_2 = int(stone[halfway:])
        return get_num_stones(half_num_1, after_blinks - 1) + get_num_stones(half_num_2, after_blinks - 1)
    else:
        return get_num_stones(stone * 2024, after_blinks - 1)


def solve(filename: str, after_blinks: int) -> int:
    with open(filename) as lines:
        line = list(lines)[0].strip().split()

    total = 0
    for stone in line:
        total += get_num_stones(int(stone), after_blinks)

    return total


def solution_2024_11_A(filename: str) -> int:
    return solve(filename, 25)


def solution_2024_11_B(filename: str) -> int:
    return solve(filename, 75)


def test_solution_2024_11_A():
    assert solution_2024_11_A("./2024_11/test_input.txt") == 55312  # Replace with expected output for the test case


# def test_final_solution_2024_11_A():
#    assert solution_2024_11_A('./2024_11/input.txt') == 0 # Replace with solution when known


# def test_solution_2024_11_B():
#    assert solution_2024_11_B("./2024_11/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_11_B():
#    assert solution_2024_11_B('./2024_11/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_11", sys.argv[1], solution_2024_11_A, solution_2024_11_B)
