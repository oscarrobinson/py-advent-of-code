import sys
from common.utils import run


def get_dmg_groups(cond_record: str) -> list[int]:
    dmg_groups = []
    current_group = 0
    for char in list(cond_record):
        if char == "?":
            break
        elif char == "." and current_group > 0:
            dmg_groups.append(current_group)
            current_group = 0
        elif char == "#":
            current_group += 1
    if current_group > 0:
        dmg_groups.append(current_group)

    return dmg_groups


def fill_first_unknown_with(cond_record: str, broken: bool) -> str:
    new_cond_record = []
    done = False
    for char in list(cond_record):
        if char == "?" and not done:
            done = True
            if broken:
                new_cond_record.append("#")
            else:
                new_cond_record.append(".")
        else:
            new_cond_record.append(char)
    return "".join(new_cond_record)


def fill_first_unknown_fixed(cond_record: str) -> str:
    return fill_first_unknown_with(cond_record, broken=False)


def test_fill_first_unknown_fixed():
    assert fill_first_unknown_fixed("#..#..??#") == "#..#...?#"


def fill_first_unknown_broken(cond_record: str) -> str:
    return fill_first_unknown_with(cond_record, broken=True)


def test_fill_first_unknown_broken():
    assert fill_first_unknown_broken("#..#..??#") == "#..#..#?#"


def test_fill_first_unknown_broken_does_nothing_if_no_unknowns():
    assert fill_first_unknown_broken("#..#..#") == "#..#..#"


def contains_unknowns(dmg_group: str) -> bool:
    return "?" in dmg_group


def is_dmg_group_poss(dmg_groups: list[int], expected_dmg_groups: list[int]) -> bool:
    if len(dmg_groups) > len(expected_dmg_groups):
        return False

    for i in range(0, len(dmg_groups)):
        try:
            # This bit of our dmg group is longer than the expected group at this position
            # Therefore it's not valid
            if dmg_groups[i] > expected_dmg_groups[i]:
                return False
            # This bit of the dmg group is complete but is shorter than expected for this part
            # And it's not the last group so it's not that we haven't finished filling that group
            # Therefore it's not valid
            elif dmg_groups[i] < expected_dmg_groups[i] and i < (len(dmg_groups) - 1):
                return False
        except IndexError:
            return False
    return True


def calc_arrangements(cond_record: str, expected_dmg_groups: list[int]) -> int:
    dmg_groups = get_dmg_groups(cond_record)

    if dmg_groups == expected_dmg_groups and not contains_unknowns(cond_record):
        return 1
    elif not is_dmg_group_poss(dmg_groups, expected_dmg_groups):
        return 0
    elif contains_unknowns(cond_record):
        return calc_arrangements(fill_first_unknown_broken(cond_record), expected_dmg_groups) + calc_arrangements(
            fill_first_unknown_fixed(cond_record), expected_dmg_groups
        )
    else:
        return 0


def get_cond_record(line: str) -> str:
    split_l = line.split(" ")
    return split_l[0]


def get_expected_dmg_groups(line: str) -> list[int]:
    split_l = line.split(" ")
    return [int(g) for g in split_l[1].split(",")]


def unfold_cond_record(cond_record: str) -> str:
    new_cond_record = []
    for i in range(0, 5):
        new_cond_record.append(cond_record)
    return "?".join(new_cond_record)


def unfold_dmg_groups(dmg_groups: list[int]) -> list[int]:
    new_dmg_groups = []
    for i in range(0, 5):
        for g in dmg_groups:
            new_dmg_groups.append(g)
    return new_dmg_groups


def solution_2023_12_A(filename: str) -> int:
    with open(filename) as file:
        result = 0
        for line in file:
            result += calc_arrangements(get_cond_record(line), get_expected_dmg_groups(line))
    return result


def solution_2023_12_B(filename: str) -> int:
    with open(filename) as file:
        result = 0
        for line in file:
            result += calc_arrangements(
                unfold_cond_record(get_cond_record(line)), unfold_dmg_groups(get_expected_dmg_groups(line))
            )
    return result


def test_solution_2023_12_A():
    assert solution_2023_12_A("./2023_12/test_input.txt") == 21  # Replace with expected output for the test case


def test_final_solution_2023_12_A():
    assert solution_2023_12_A("./2023_12/input.txt") == 7622  # Replace with solution when known


# Very slow currently so commented out
# def test_solution_2023_12_B():
#    assert solution_2023_12_B("./2023_12/test_input.txt") == 525152  # Replace with expected output for the test case
#

# def test_final_solution_2023_12_B():
#    assert solution_2023_12_B('./2023_12/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2023_12", sys.argv[1], solution_2023_12_A, solution_2023_12_B)
