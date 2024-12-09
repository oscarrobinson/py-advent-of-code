import sys
from common.utils import run


def solution_2024_09_A(filename: str) -> int:
    with open(filename) as lines:
        compact_disk_map = list(int(char) for char in "".join([line for line in lines]))
    disk_map = []
    for n, length in enumerate(compact_disk_map):
        is_file = n % 2 == 0
        file_id = int(n / 2)
        for i in range(0, length):
            if is_file:
                disk_map.append(file_id)
            else:
                disk_map.append(-1)

    i_desc = len(disk_map) - 1
    i_asc = 0

    while i_asc < i_desc:
        is_empty_block = disk_map[i_asc] == -1
        if is_empty_block:
            while disk_map[i_desc] == -1:
                i_desc -= 1
            if i_asc < i_desc:
                tmp = disk_map[i_desc]
                disk_map[i_desc] = disk_map[i_asc]
                disk_map[i_asc] = tmp
        i_asc += 1

    checksum = 0
    checksum_i = 0
    while disk_map[checksum_i] != -1:
        checksum += disk_map[checksum_i] * checksum_i
        checksum_i += 1

    return checksum


def solution_2024_09_B(filename: str) -> int:
    return 0


def test_solution_2024_09_A():
    assert solution_2024_09_A("./2024_09/test_input.txt") == 1928  # Replace with expected output for the test case


# def test_final_solution_2024_09_A():
#    assert solution_2024_09_A('./2024_09/input.txt') == 0 # Replace with solution when known


def test_solution_2024_09_B():
    assert solution_2024_09_B("./2024_09/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_09_B():
#    assert solution_2024_09_B('./2024_09/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_09", sys.argv[1], solution_2024_09_A, solution_2024_09_B)
