import sys
from common.utils import run
from common.grid import grid_from_lines, Grid, Point
from collections import deque
from functools import cache

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

raw_numeric_grid = ["789", "456", "123", ".0A"]

raw_directional_grid = [".^A", "<v>"]

numeric_grid = grid_from_lines(raw_numeric_grid)
directional_grid = grid_from_lines(raw_directional_grid)


def neighbours_with_direction(buttons: Grid, point: Point) -> list[(str, Point)]:
    all_neighbours = buttons.get_all_neighbours(point)
    neighbours_with_dir = [
        ("^", all_neighbours[0]),
        ("v", all_neighbours[1]),
        ("<", all_neighbours[2]),
        (">", all_neighbours[3]),
    ]
    result = []
    for neighbour_with_dir in neighbours_with_dir:
        if neighbour_with_dir[1] is not None and buttons.val(neighbour_with_dir[1].point) != ".":
            result.append((neighbour_with_dir[0], neighbour_with_dir[1].point))
    return result


@cache
def get_shortest_press_seq_between(source: str, target: str, buttons: Grid) -> list[str]:
    source_pos = buttons.find_point_with_val(source)
    queue = deque()
    visited = set()
    queue.append((source_pos, []))
    while queue:
        loc, press_seq = queue.popleft()
        visited.add(loc)
        if buttons.val(loc) == target:
            return press_seq + ["A"]
        for direction, neighbour in neighbours_with_direction(buttons, loc):
            if neighbour not in visited:
                queue.append((neighbour, press_seq + [direction]))


def get_shortest_press_seq(target_seq: str, buttons: Grid) -> str:
    cur_point = "A"
    press_seq = []
    for target_point in target_seq:
        add_seq = get_shortest_press_seq_between(cur_point, target_point, buttons)
        press_seq = press_seq + add_seq
        cur_point = target_point
    return "".join(press_seq)


def shortest_press_seq_length(numeric_seq: str) -> int:
    robot_1_press_seq = get_shortest_press_seq(numeric_seq, numeric_grid)

    robot_2_press_seq = get_shortest_press_seq(robot_1_press_seq, directional_grid)

    robot_3_press_seq = get_shortest_press_seq(robot_2_press_seq, directional_grid)
    print(numeric_seq)
    print(robot_1_press_seq)
    print(robot_2_press_seq)
    print(robot_3_press_seq)
    print("-----------")
    return len(get_shortest_press_seq(robot_3_press_seq, directional_grid))


def solution_2024_21_A(filename: str) -> int:
    result = 0
    with open(filename) as lines:
        for line in lines:
            length = shortest_press_seq_length(line.strip())
            # all input lines are three digits followed by A so just be lazy here...
            num_part = int(line[0:3])
            result += num_part * length
    return result


def solution_2024_21_B(filename: str) -> int:
    return 0


def test_solution_2024_21_A():
    assert solution_2024_21_A("./2024_21/test_input.txt") == 126384  # Replace with expected output for the test case


# def test_final_solution_2024_21_A():
#    assert solution_2024_21_A('./2024_21/input.txt') == 0 # Replace with solution when known


def test_solution_2024_21_B():
    assert solution_2024_21_B("./2024_21/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_21_B():
#    assert solution_2024_21_B('./2024_21/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_21", sys.argv[1], solution_2024_21_A, solution_2024_21_B)
