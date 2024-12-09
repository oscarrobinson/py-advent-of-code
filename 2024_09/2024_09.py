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

    while i_desc > 0:
        if disk_map[i_desc] != -1:
            # lookahead to get file length
            file_val = disk_map[i_desc]
            lookahead_i_desc = i_desc
            while disk_map[lookahead_i_desc] == file_val:
                lookahead_i_desc -= 1

            file_length = i_desc - lookahead_i_desc

            # See if we have a position to put the file
            i_asc = 0

            nowhere_for_file = True

            while i_asc < i_desc:
                if disk_map[i_asc] == -1:
                    # lookahead to get the empty length
                    lookahead_i_asc = i_asc
                    while disk_map[lookahead_i_asc] == -1:
                        lookahead_i_asc += 1

                    empty_length = lookahead_i_asc - i_asc

                    if empty_length >= file_length:
                        for i in range(0, file_length):
                            tmp = disk_map[i_desc]
                            disk_map[i_desc] = disk_map[i_asc]
                            disk_map[i_asc] = tmp
                            i_desc -= 1
                            i_asc += 1
                        # we moved the file and i_desc is now correctly past the file, we can break out of this loop
                        nowhere_for_file = False
                        break
                    else:
                        # we keep looking for somewhere to put the file
                        # update i_asc to skip over this whole empty chunk
                        i_asc += empty_length
                else:
                    # it's a file block, so let's go to the next block
                    i_asc += 1

            if nowhere_for_file:
                # decrement i_desc to skip the file
                i_desc -= file_length
        else:
            i_desc -= 1

    checksum = 0

    for i, file_id in enumerate(disk_map):
        if file_id != -1:
            checksum += i * file_id

    return checksum


def test_solution_2024_09_A():
    assert solution_2024_09_A("./2024_09/test_input.txt") == 1928  # Replace with expected output for the test case


# def test_final_solution_2024_09_A():
#    assert solution_2024_09_A('./2024_09/input.txt') == 0 # Replace with solution when known


def test_solution_2024_09_B():
    assert solution_2024_09_B("./2024_09/test_input.txt") == 2858  # Replace with expected output for the test case


# def test_final_solution_2024_09_B():
#    assert solution_2024_09_B('./2024_09/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_09", sys.argv[1], solution_2024_09_A, solution_2024_09_B)
