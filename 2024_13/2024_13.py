import sys
import re
import numpy as np
from common.utils import run


# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# 94a + 22b = 8400
# 34a + 67b = 5400
# If can solve for a and b as integers then these buttons can reach prize


def to_int_or_none(num) -> int | None:
    int_part, dec_part = str(np.round(num, 3)).split(".")
    if dec_part != "0":
        return None
    else:
        return int(int_part)


def solution_2024_13_A(filename: str) -> int:
    with open(filename) as lines:
        lines = list(lines)

    button_rgx = re.compile("Button [A|B]{1}: X\\+([0-9]+), Y\\+([0-9]+)")
    prize_rgx = re.compile("Prize: X=([0-9]+), Y=([0-9]+)")

    total_spend = 0

    for i in range(0, len(lines), 4):
        a1, a2 = button_rgx.match(lines[i]).group(1, 2)
        b1, b2 = button_rgx.match(lines[i + 1]).group(1, 2)
        eq1, eq2 = prize_rgx.match(lines[i + 2]).group(1, 2)

        # print("Equations to solve, where 'a' is number of presses of A and 'b' is number of presses of B:")
        # print(f"{a1}a + {b1}b = {eq1}")
        # print(f"{a2}a + {b2}b = {eq2}")

        a = np.array([[int(a1), int(b1)], [int(a2), int(b2)]])
        b = np.array([int(eq1), int(eq2)])
        a_presses, b_presses = [to_int_or_none(num) for num in np.linalg.solve(a, b)]

        if a_presses and b_presses:
            total_spend += a_presses * 3
            total_spend += b_presses

    return total_spend


def solution_2024_13_B(filename: str) -> int:
    with open(filename) as lines:
        lines = list(lines)

    button_rgx = re.compile("Button [A|B]{1}: X\\+([0-9]+), Y\\+([0-9]+)")
    prize_rgx = re.compile("Prize: X=([0-9]+), Y=([0-9]+)")

    total_spend = 0

    for i in range(0, len(lines), 4):
        a1, a2 = button_rgx.match(lines[i]).group(1, 2)
        b1, b2 = button_rgx.match(lines[i + 1]).group(1, 2)
        eq1, eq2 = prize_rgx.match(lines[i + 2]).group(1, 2)

        # print("Equations to solve, where 'a' is number of presses of A and 'b' is number of presses of B:")
        # print(f"{a1}a + {b1}b = {eq1}")
        # print(f"{a2}a + {b2}b = {eq2}")

        a = np.array([[int(a1), int(b1)], [int(a2), int(b2)]])
        b = np.array([int(eq1) + 10000000000000, int(eq2) + 10000000000000])
        a_presses, b_presses = [to_int_or_none(num) for num in np.linalg.solve(a, b)]

        if a_presses and b_presses:
            total_spend += a_presses * 3
            total_spend += b_presses

    return total_spend


def test_solution_2024_13_A():
    assert solution_2024_13_A("./2024_13/test_input.txt") == 480  # Replace with expected output for the test case


# def test_final_solution_2024_13_A():
#    assert solution_2024_13_A('./2024_13/input.txt') == 0 # Replace with solution when known


def test_solution_2024_13_B():
    assert (
        solution_2024_13_B("./2024_13/test_input.txt") == 875318608908
    )  # Replace with expected output for the test case


# def test_final_solution_2024_13_B():
#    assert solution_2024_13_B('./2024_13/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_13", sys.argv[1], solution_2024_13_A, solution_2024_13_B)
