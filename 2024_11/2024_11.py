import sys
from common.utils import run
from functools import lru_cache


@lru_cache(maxsize=1000000)
def get_next_numbers(num_str: str) -> list[str]:
    new_nums = []
    if int(num_str) == 0:
        new_nums.append("1")
    elif len(num_str) % 2 == 0:
        new_nums.append(str(int(num_str[0 : int(len(num_str) / 2)])))
        new_nums.append(str(int(num_str[int(len(num_str) / 2) :])))
    else:
        new_nums.append(str(int(num_str) * 2024))
    return new_nums


def get_num_stones(filename: str, after_blinks: int) -> int:
    with open(filename) as lines:
        line = list(lines)[0].strip().split()

    for i in range(0, after_blinks):
        print("\n--------\n")
        print(get_next_numbers.cache_info())
        print(i)
        new_line = []
        j = 0
        length = len(line)
        print(length)
        for num_str in line:
            j += 1
            print(str(j) + "\r", end="")
            for num in get_next_numbers(num_str):
                new_line.append(num)
        line = new_line

    return len(line)


def solution_2024_11_A(filename: str) -> int:
    return get_num_stones(filename, 25)


# TODO: Cache grows very slowly, this means same numbers come up again and again
# each application of the rules must form a cycle


def solution_2024_11_B(filename: str) -> int:
    return get_num_stones(filename, 75)


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
