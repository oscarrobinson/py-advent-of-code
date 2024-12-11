import sys
from common.utils import run


def get_num_stones(filename: str, after_blinks: int) -> int:
    with open(filename) as lines:
        line = list(lines)[0].strip().split()

    for i in range(0, after_blinks):
        print(i)
        new_line = []
        for num_str in line:
            if int(num_str) == 0:
                new_line.append("1")
            elif len(num_str) % 2 == 0:
                new_line.append(str(int(num_str[0 : int(len(num_str) / 2)])))
                new_line.append(str(int(num_str[int(len(num_str) / 2) :])))
            else:
                new_line.append(str(int(num_str) * 2024))
        line = new_line

    return len(line)


def solution_2024_11_A(filename: str) -> int:
    return get_num_stones(filename, 25)


def solution_2024_11_B(filename: str) -> int:
    return 0
    # return get_num_stones(filename, 75)


def test_solution_2024_11_A():
    assert solution_2024_11_A("./2024_11/test_input.txt") == 55312  # Replace with expected output for the test case


# def test_final_solution_2024_11_A():
#    assert solution_2024_11_A('./2024_11/input.txt') == 0 # Replace with solution when known


# def test_solution_2024_11_B():
#    assert solution_2024_11_B("./2024_11/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_11_B():
#    assert solution_2024_11_B('./2024_11/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_11", sys.argv[1], solution_2024_11_A, solution_2024_11_B)
