import sys
from common.utils import run
from collections import Counter


def parse_numbers(lines: list[str]) -> (list[int], list[int]):
    nums1 = []
    nums2 = []
    for line in lines:
        num1, num2 = line.split()
        nums1.append(int(num1))
        nums2.append(int(num2))
    return (nums1, nums2)


def solution_2024_01_A(filename: str) -> int:
    with open(filename) as file:
        total = 0
        nums1, nums2 = parse_numbers(list(file))
        nums1.sort()
        nums2.sort()

        for i in range(0, len(nums1)):
            total += abs(nums1[i] - nums2[i])
        return total


def solution_2024_01_B(filename: str) -> int:
    with open(filename) as file:
        total = 0
        nums1, nums2 = parse_numbers(list(file))
        counts = Counter(nums2)
        for num in nums1:
            total += num * counts[num]
        return total


def test_solution_2024_01_A():
    assert solution_2024_01_A("./2024_01/test_input.txt") == 11  # Replace with expected output for the test case


def test_final_solution_2024_01_A():
    assert solution_2024_01_A("./2024_01/input.txt") == 1970720  # Replace with solution when known


def test_solution_2024_01_B():
    assert solution_2024_01_B("./2024_01/test_input.txt") == 31  # Replace with expected output for the test case


def test_final_solution_2024_01_B():
    assert solution_2024_01_B("./2024_01/input.txt") == 17191599  # Replace with solution when known


if __name__ == "__main__":
    run("2024_01", sys.argv[1], solution_2024_01_A, solution_2024_01_B)
