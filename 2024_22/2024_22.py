import sys
from common.utils import run


# Calculate the result of multiplying the secret number by 64.
# Then, mix this result into the secret number. Finally, prune the secret number.
#
# Calculate the result of dividing the secret number by 32.
# Round the result down to the nearest integer.
# Then, mix this result into the secret number. Finally, prune the secret number.
#
# Calculate the result of multiplying the secret number by 2048.
# Then, mix this result into the secret number. Finally, prune the secret number.
# Each step of the above process involves mixing and pruning:
#
# To mix a value into the secret number,
# calculate the bitwise XOR of the given value and the secret number.
# Then, the secret number becomes the result of that operation.
# (If the secret number is 42 and you were to mix 15 into the secret number,
# the secret number would become 37.)
#
# To prune the secret number,
# calculate the value of the secret number modulo 16777216.
# Then, the secret number becomes the result of that operation.
# (If the secret number is 100000000 and you were to prune the secret number,
# the secret number would become 16113920.)


def get_nth_secret_number(initial: int, n: int) -> int:
    secret = initial
    for _ in range(0, n):
        step_1 = secret << 6  # multiply 64
        step_2 = step_1 ^ secret  # mix
        step_3 = step_2 % 16777216  # prune (16777216 is 2^24 so may be a more efficient modulo somehow)
        step_4 = step_3 >> 5  # divide 32
        step_5 = step_4 ^ step_3  # mix
        step_6 = step_5 % 16777216  # prune
        step_7 = step_6 << 11  # multiply 2048
        step_8 = step_7 ^ step_6  # mix
        secret = step_8 % 16777216  # prune
    return secret


def solution_2024_22_A(filename: str) -> int:
    total = 0
    with open(filename) as lines:
        for line in lines:
            initial = int(line.strip())
            total += get_nth_secret_number(initial, 2000)
    return total


def solution_2024_22_B(filename: str) -> int:
    return 0


def test_solution_2024_22_A():
    assert solution_2024_22_A("./2024_22/test_input.txt") == 37327623  # Replace with expected output for the test case


# def test_final_solution_2024_22_A():
#    assert solution_2024_22_A('./2024_22/input.txt') == 0 # Replace with solution when known


def test_solution_2024_22_B():
    assert solution_2024_22_B("./2024_22/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_22_B():
#    assert solution_2024_22_B('./2024_22/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_22", sys.argv[1], solution_2024_22_A, solution_2024_22_B)
