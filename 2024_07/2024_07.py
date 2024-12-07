import sys
from common.utils import run


def is_valid_eq(exp_result: int, nums: list[int]) -> bool:
    # DFS to find a valid eq
    stack = []
    stack.append((nums[0], nums[1:]))
    while stack:
        running_result, rem_nums = stack.pop()
        if len(rem_nums) == 0:
            if running_result == exp_result:
                return True
        elif running_result <= exp_result:
            stack.append((running_result * rem_nums[0], rem_nums[1:]))
            stack.append((running_result + rem_nums[0], rem_nums[1:]))
    # Our DFS found no combo of operators that solved the equation
    # Therefore the equation is not valid so return False
    return False


def solution_2024_07_A(filename: str) -> int:
    result = 0
    with open(filename) as lines:
        for line in lines:
            raw_eq_result, raw_eq = line.split(":")
            eq_result = int(raw_eq_result)
            eq_nums = [int(num.strip()) for num in raw_eq.split() if "\n" not in num]
            if is_valid_eq(eq_result, eq_nums):
                result += eq_result
    return result


def is_valid_eq_b(exp_result: int, nums: list[int]) -> bool:
    # DFS to find a valid eq
    stack = []
    stack.append((nums[0], nums[1:]))
    while stack:
        running_result, rem_nums = stack.pop()
        if len(rem_nums) == 0:
            if running_result == exp_result:
                return True
        elif running_result <= exp_result:
            stack.append((running_result * rem_nums[0], rem_nums[1:]))
            stack.append((running_result + rem_nums[0], rem_nums[1:]))
            # || concat operator
            stack.append((int(str(running_result) + str(rem_nums[0])), rem_nums[1:]))
    # Our DFS found no combo of operators that solved the equation
    # Therefore the equation is not valid so return False
    return False


def solution_2024_07_B(filename: str) -> int:
    result = 0
    with open(filename) as lines:
        for line in lines:
            raw_eq_result, raw_eq = line.split(":")
            eq_result = int(raw_eq_result)
            eq_nums = [int(num.strip()) for num in raw_eq.split() if "\n" not in num]
            if is_valid_eq_b(eq_result, eq_nums):
                result += eq_result
    return result


def test_solution_2024_07_A():
    assert solution_2024_07_A("./2024_07/test_input.txt") == 3749  # Replace with expected output for the test case


def test_final_solution_2024_07_A():
    assert solution_2024_07_A("./2024_07/input.txt") == 1289579105366  # Replace with solution when known


def test_solution_2024_07_B():
    assert solution_2024_07_B("./2024_07/test_input.txt") == 11387  # Replace with expected output for the test case


# def test_final_solution_2024_07_B():
#    assert solution_2024_07_B('./2024_07/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_07", sys.argv[1], solution_2024_07_A, solution_2024_07_B)
