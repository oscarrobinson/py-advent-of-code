import sys
import re
from common.utils import run


def execute_mul(mul_instr: str) -> int:
    num1, num2 = mul_instr.split(",")
    return int(num1[4:]) * int(num2[:-1])


def solution_2024_03_A(filename: str) -> int:
    with open(filename) as file:
        mem = file.read().replace("\n", "")
        pattern = r"mul\([0-9]+,[0-9]+\)"
        matches = re.findall(pattern, mem)
        return sum([execute_mul(instr) for instr in matches])


def solution_2024_03_B(filename: str) -> int:
    return 0


def test_solution_2024_03_A():
    assert solution_2024_03_A("./2024_03/test_input.txt") == 161  # Replace with expected output for the test case


# def test_final_solution_2024_03_A():
#    assert solution_2024_03_A('./2024_03/input.txt') == 0 # Replace with solution when known


def test_solution_2024_03_B():
    assert solution_2024_03_B("./2024_03/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_03_B():
#    assert solution_2024_03_B('./2024_03/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_03", sys.argv[1], solution_2024_03_A, solution_2024_03_B)
