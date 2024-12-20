import sys
from common.utils import run
from common.grid import grid_from_lines, min_distance

START = "S"
END = "E"
WALL = "#"


def solution_2024_20_A(filename: str, min_saving=100) -> int:
    with open(filename) as file:
        lines = list(file)
    track = grid_from_lines(lines)

    start = [cell.point for cell in track if cell.val == START][0]

    # fill each path cell with dist from start
    visited = set()
    stack = [start]

    i = 0
    while stack:
        loc = stack.pop()
        track.set_val(loc, str(i))
        visited.add(loc)
        neighbours = track.get_neighbours(loc)
        for neighbour in neighbours:
            if neighbour.val != WALL and neighbour.point not in visited:
                stack.append(neighbour.point)
        i += 1

    # visit each visited cell on the track and find any points within 2 moves that
    # are not walls and have a value > the value of that cell, this is a valid cheat
    big_cheats_count = 0

    for loc in visited:
        loc_i = int(track.val(loc))
        for n1 in track.get_neighbours(loc):
            for n2 in track.get_neighbours(n1.point):
                if n2.val != WALL and int(n2.val) > loc_i + 2:
                    # subtract 2 cos we still moved 2 places while cheating
                    # so saved the difference between the two points minus the 2 places we moved
                    # during the cheat.
                    if int(n2.val) - loc_i - 2 >= min_saving:
                        big_cheats_count += 1

    return big_cheats_count


def solution_2024_20_B(filename: str, min_saving=100) -> int:
    with open(filename) as file:
        lines = list(file)
    track = grid_from_lines(lines)

    start = [cell.point for cell in track if cell.val == START][0]

    # fill each path cell with dist from start
    visited = list()
    visited_set = set()
    stack = [start]

    i = 0
    while stack:
        loc = stack.pop()
        track.set_val(loc, str(i))
        visited.append(loc)
        visited_set.add(loc)
        neighbours = track.get_neighbours(loc)
        for neighbour in neighbours:
            if neighbour.val != WALL and neighbour.point not in visited_set:
                stack.append(neighbour.point)
        i += 1

    # visit each visited cell on the track and find all other points on the track that
    # have a distance <= 20 and result in a saving >= min_saving
    big_cheats_count = 0
    max_cheat_dist = 20
    i = 0
    for loc in visited:
        i += 1
        print(f"{i}/{len(visited)}", end="\r")
        for other_loc in visited:
            dist = min_distance(loc, other_loc)
            other_loc_val = int(track.val(other_loc))
            loc_val = int(track.val(loc))
            if (other_loc_val - loc_val - dist) >= min_saving and dist <= max_cheat_dist:
                big_cheats_count += 1

    return big_cheats_count


def test_solution_2024_20_A():
    assert (
        solution_2024_20_A("./2024_20/test_input.txt", min_saving=20) == 5
    )  # Replace with expected output for the test case


# def test_final_solution_2024_20_A():
#    assert solution_2024_20_A('./2024_20/input.txt') == 0 # Replace with solution when known


def test_solution_2024_20_B():
    assert (
        solution_2024_20_B("./2024_20/test_input.txt", min_saving=64) == 86
    )  # Replace with expected output for the test case


# def test_final_solution_2024_20_B():
#    assert solution_2024_20_B('./2024_20/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_20", sys.argv[1], solution_2024_20_A, solution_2024_20_B)
