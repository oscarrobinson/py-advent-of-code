import sys
import itertools
from common.utils import run
from common.grid import Point, grid_from_lines
from collections import defaultdict


EMPTY = "."


def solution_2024_08_A(filename: str) -> int:
    with open(filename) as file:
        antenna_map = grid_from_lines(list(file))
        antenna_locs = defaultdict(list)
        for loc in antenna_map:
            if loc.val != EMPTY:
                antenna_locs[loc.val].append(loc.point)
        antenna_pairs_lists = [list(itertools.permutations(locs, 2)) for locs in antenna_locs.values()]
        # This duplicates pairs e.g ((0,1),(2,3)) and ((2,3),(0,1))
        # But doesn't matter if we add discovered antinodes to a set
        antenna_pairs = [pair for ant_pairs in antenna_pairs_lists for pair in ant_pairs]
        antinodes = set()
        for pair in antenna_pairs:
            top, bottom = (pair[0], pair[1]) if pair[0].y < pair[1].y else (pair[1], pair[0])
            diff_x = pair[0].x - pair[1].x
            diff_y = bottom.y - top.y
            if top.x > bottom.x:
                # / diagnoal
                antinode_1 = (top.x + abs(diff_x), top.y - diff_y)
                if not antenna_map.val(Point(antinode_1[0], antinode_1[1])) == "OUT_OF_BOUNDS":
                    antinodes.add(antinode_1)
                antinode_2 = (bottom.x - abs(diff_x), bottom.y + diff_y)
                if not antenna_map.val(Point(antinode_2[0], antinode_2[1])) == "OUT_OF_BOUNDS":
                    antinodes.add(antinode_2)
            else:
                # | or \ diagonal
                antinode_1 = antinode_1 = (top.x - abs(diff_x), top.y - diff_y)
                if not antenna_map.val(Point(antinode_1[0], antinode_1[1])) == "OUT_OF_BOUNDS":
                    antinodes.add(antinode_1)
                antinode_2 = (bottom.x + abs(diff_x), bottom.y + diff_y)
                if not antenna_map.val(Point(antinode_2[0], antinode_2[1])) == "OUT_OF_BOUNDS":
                    antinodes.add(antinode_2)
        return len(antinodes)


def solution_2024_08_B(filename: str) -> int:
    return 0


def test_solution_2024_08_A():
    assert solution_2024_08_A("./2024_08/test_input.txt") == 14  # Replace with expected output for the test case


# def test_final_solution_2024_08_A():
#    assert solution_2024_08_A('./2024_08/input.txt') == 0 # Replace with solution when known


def test_solution_2024_08_B():
    assert solution_2024_08_B("./2024_08/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_08_B():
#    assert solution_2024_08_B('./2024_08/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_08", sys.argv[1], solution_2024_08_A, solution_2024_08_B)
