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
def get_shortest_press_seqs_between(source: str, target: str, buttons: Grid) -> list[list[str]]:
    source_pos = buttons.find_point_with_val(source)
    queue = deque()
    visited = set()
    shortest_path_len = None
    queue.append((source_pos, []))
    results = []
    while queue:
        loc, press_seq = queue.popleft()
        visited.add(loc)
        if buttons.val(loc) == target:
            final_path = press_seq + ["A"]
            if not shortest_path_len:
                shortest_path_len = len(final_path)
            if len(final_path) == shortest_path_len:
                results.append(final_path)
        for direction, neighbour in neighbours_with_direction(buttons, loc):
            if neighbour not in visited:
                queue.append((neighbour, press_seq + [direction]))
    return results


@cache
def get_shortest_press_seqs(cur_button: str, rem_seq: str, buttons: Grid) -> list[str]:
    if len(rem_seq) == 1:
        return ["".join(seq) for seq in get_shortest_press_seqs_between(cur_button, rem_seq, buttons)]
    else:
        result = []
        header_paths = get_shortest_press_seqs_between(cur_button, rem_seq[0], buttons)
        # only bother including shortest header paths
        len_shortest_header_path = min([len(path) for path in header_paths])
        for header in header_paths:
            if len(header) == len_shortest_header_path:
                poss_subsequent_paths = get_shortest_press_seqs(rem_seq[0:1], rem_seq[1:], buttons)
                for sub_path in poss_subsequent_paths:
                    result.append("".join(header) + sub_path)
        return result


#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

press_dist_mapping = {
    "<": {"v": 1, "^": 2, ">": 2, "A": 3, "<": 0},
    "v": {"<": 1, ">": 1, "^": 1, "A": 2, "v": 0},
    ">": {"v": 1, "A": 1, "^": 2, "<": 2, ">": 0},
    "^": {"A": 1, "v": 1, ">": 2, "<": 2, "^": 0},
    "A": {"^": 1, ">": 1, "v": 2, "<": 3, "A": 0},
}


def directional_press_seq_to_length(press_seq: str) -> int:
    total = 0
    for i in range(0, len(press_seq) - 2):
        cur_button = press_seq[i]
        next_button = press_seq[i + 1]
        dist = press_dist_mapping[cur_button][next_button]
        total += dist
        total += 1  # +1 cos we need to press A to then make the robot press the button
    return total


def shortest_press_seq_length(numeric_seq: str) -> int:
    robot_1_press_seqs = get_shortest_press_seqs("A", numeric_seq, numeric_grid)
    robot_2_press_seqs = [
        final_seq for seq in robot_1_press_seqs for final_seq in get_shortest_press_seqs("A", seq, directional_grid)
    ]
    robot_3_press_seqs = [
        final_seq for seq in robot_2_press_seqs for final_seq in get_shortest_press_seqs("A", seq, directional_grid)
    ]
    return min([len(seq) for seq in robot_3_press_seqs])


def solution_2024_21_A(filename: str) -> int:
    result = 0
    with open(filename) as lines:
        for line in list(lines):
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
