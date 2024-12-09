import sys
from common.utils import run


def solution_2024_09_A(filename: str) -> int:
    with open(filename) as lines:
        disk_map = list(int(char) for char in "".join([line for line in lines]))
        print(disk_map)
    new_disk_map = []
    checksum = 0
    for i, block_group_length in enumerate(disk_map):
        is_file = (i % 2) == 0
        if is_file:
            file_id = i / 2
            new_disk_map.append(block_group_length)
            for n in range(0, block_group_length):
                checksum += file_id * n
        else:
            pass
            # empty of length block_group_length
            # TODO: Store index and value of which file we're stealing blocks
            # while taking_from_file is not empty and taking_from_file != current block we're looking at:
            #    take block_group_length blocks from that file
            #    append to new_disk_map
            #    update checksum
            #    if taking_from_file is empty:
            #       get the next file
    return 0


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
