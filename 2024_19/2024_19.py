import sys
from common.utils import run
from functools import cache


def solution_2024_19_A(filename: str) -> int:
    with open(filename) as file:
        lines = list(file)
    patterns = set([raw_towel.strip() for raw_towel in lines[0].split(",")])
    designs = [line.strip() for line in lines[2:]]

    total_possible = 0

    for design in designs:
        stack = [design]
        had_on_stack = {design}
        while stack:
            rem_design = stack.pop()
            if rem_design == "":
                total_possible += 1
                break
            else:
                for pattern in patterns:
                    l_d = len(rem_design)
                    l_p = len(pattern)
                    if l_d >= l_p and rem_design[0:l_p] == pattern:
                        new_rem_design = rem_design[l_p:]
                        if new_rem_design not in had_on_stack:
                            had_on_stack.add(new_rem_design)
                            stack.append(rem_design[l_p:])

    return total_possible


def solution_2024_19_B(filename: str) -> int:
    with open(filename) as file:
        lines = list(file)
    patterns = ",".join(list([raw_towel.strip() for raw_towel in lines[0].split(",")]))
    designs = [line.strip() for line in lines[2:]]

    total_possible = 0

    @cache
    def count_poss_combos(rem_design: str, patterns_str: str):
        patterns = set(patterns_str.split(","))
        if rem_design == "":
            return 1
        else:
            rem_design_poss = []
            for pattern in patterns:
                l_d = len(rem_design)
                l_p = len(pattern)
                if l_d >= l_p and rem_design[0:l_p] == pattern:
                    rem_design_poss.append(rem_design[l_p:])
            if rem_design_poss == []:
                return 0
            else:
                return sum([count_poss_combos(rem, patterns_str) for rem in rem_design_poss])

    for design in designs:
        total_possible += count_poss_combos(design, patterns)

    return total_possible


def test_solution_2024_19_A():
    assert solution_2024_19_A("./2024_19/test_input.txt") == 6  # Replace with expected output for the test case


# def test_final_solution_2024_19_A():
#    assert solution_2024_19_A('./2024_19/input.txt') == 0 # Replace with solution when known


def test_solution_2024_19_B():
    assert solution_2024_19_B("./2024_19/test_input.txt") == 16  # Replace with expected output for the test case


# def test_final_solution_2024_19_B():
#    assert solution_2024_19_B('./2024_19/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_19", sys.argv[1], solution_2024_19_A, solution_2024_19_B)
