import sys
from common.utils import run


def is_safe(report: str) -> bool:
    report = [int(r) for r in report.split()]
    sorted_rep = sorted(report)
    sorted_rep_desc = sorted(report, reverse=True)

    if not (sorted_rep == report or sorted_rep_desc == report):
        return False
    else:
        differences = [abs(i - j) for i, j in zip(report, report[1:])]
        return all([((diff >= 1) and (diff <= 3)) for diff in differences])


def test_is_safe():
    reports = [
        ("7 6 4 2 1", True),
        ("1 2 7 8 9", False),
        ("9 7 6 2 1", False),
        ("1 3 2 4 5", False),
        ("8 6 4 4 1", False),
        ("1 3 6 7 9", True),
    ]
    for report, rep_is_safe in reports:
        assert is_safe(report) == rep_is_safe


def solution_2024_02_A(filename: str) -> int:
    result = 0
    with open(filename) as lines:
        for line in lines:
            if is_safe(line):
                result += 1
    return result


def is_safe_with_tolerance(report: str) -> bool:
    if is_safe(report):
        return True

    report = [int(r) for r in report.split()]

    for i in range(0, len(report)):
        safe_with_elem_removed = is_safe(" ".join([str(x) for x in (report[:i] + report[i + 1 :])]))
        if safe_with_elem_removed:
            return True

    return False


def test_is_safe_with_tolerance():
    reports = [
        ("7 6 4 2 1", True),
        ("1 2 7 8 9", False),
        ("9 7 6 2 1", False),
        ("1 3 2 4 5", True),
        ("8 6 4 4 1", True),
        ("1 3 6 7 9", True),
    ]
    for report, rep_is_safe in reports:
        assert is_safe_with_tolerance(report) == rep_is_safe


def solution_2024_02_B(filename: str) -> int:
    result = 0
    with open(filename) as lines:
        for line in lines:
            if is_safe_with_tolerance(line):
                result += 1
    return result


def test_solution_2024_02_A():
    assert solution_2024_02_A("./2024_02/test_input.txt") == 2  # Replace with expected output for the test case


def test_final_solution_2024_02_A():
    assert solution_2024_02_A("./2024_02/input.txt") == 269  # Replace with solution when known


def test_solution_2024_02_B():
    assert solution_2024_02_B("./2024_02/test_input.txt") == 4  # Replace with expected output for the test case


# def test_final_solution_2024_02_B():
#    assert solution_2024_02_B('./2024_02/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_02", sys.argv[1], solution_2024_02_A, solution_2024_02_B)
