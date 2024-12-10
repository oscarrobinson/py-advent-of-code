import sys
from common.utils import run
from common.grid import grid_from_lines


def solution_2024_10_A(filename: str) -> int:
    with open(filename) as lines:
        trail_map = grid_from_lines(list(lines))

    trailheads = [cell for cell in trail_map if cell.val == "0"]

    total_score = 0

    for trailhead in trailheads:
        reachable_peaks = set()
        stack = [trailhead]
        while stack:
            loc = stack.pop()
            neighbours = trail_map.get_neighbours(loc.point)
            loc_height = int(loc.val)
            for neighbour in neighbours:
                neighbour_height = int(neighbour.val)
                if neighbour_height == 9 and loc_height == 9 - 1:
                    reachable_peaks.add((neighbour.point.x, neighbour.point.y))
                elif neighbour_height == loc_height + 1:
                    stack.append(neighbour)

        trailhead_score = len(reachable_peaks)
        total_score += trailhead_score

    return total_score


def solution_2024_10_B(filename: str) -> int:
    return 0


def test_solution_2024_10_A():
    assert solution_2024_10_A("./2024_10/test_input.txt") == 36  # Replace with expected output for the test case


# def test_final_solution_2024_10_A():
#    assert solution_2024_10_A('./2024_10/input.txt') == 0 # Replace with solution when known


def test_solution_2024_10_B():
    assert solution_2024_10_B("./2024_10/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_10_B():
#    assert solution_2024_10_B('./2024_10/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_10", sys.argv[1], solution_2024_10_A, solution_2024_10_B)
