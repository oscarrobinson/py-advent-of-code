import sys
import re
import math
import time
from common.utils import run


def solution_2024_14_A(filename: str) -> int:
    room_width = 101
    room_height = 103
    iterations = 100

    rgx = re.compile("p=([\\-0-9]+),([\\-0-9]+) v=([\\-0-9]+),([\\-0-9]+)")
    robots = []

    with open(filename) as lines:
        for line in lines:
            p_x, p_y, v_x, v_y = rgx.match(line).group(1, 2, 3, 4)
            robots.append((int(p_x), int(p_y), int(v_x), int(v_y)))

    final_robot_positions = []

    for robot in robots:
        p_x = (robot[0] + (robot[2] * iterations)) % room_width
        p_y = (robot[1] + (robot[3] * iterations)) % room_height
        final_robot_positions.append((p_x, p_y))

    tl_quad_count = 0
    tr_quad_count = 0
    bl_quad_count = 0
    br_quad_count = 0

    for robot in final_robot_positions:
        p_x = robot[0]
        p_y = robot[1]
        center_x = math.floor(room_width / 2)
        center_y = math.floor(room_height / 2)

        if p_x < center_x and p_y < center_y:
            tl_quad_count += 1
        elif p_x > center_x and p_y < center_y:
            tr_quad_count += 1
        elif p_x < center_x and p_y > center_y:
            bl_quad_count += 1
        elif p_x > center_x and p_y > center_y:
            br_quad_count += 1

    return tl_quad_count * tr_quad_count * bl_quad_count * br_quad_count


def solution_2024_14_B(filename: str) -> int:
    room_width = 101
    room_height = 103
    iterations = 1

    rgx = re.compile("p=([\\-0-9]+),([\\-0-9]+) v=([\\-0-9]+),([\\-0-9]+)")
    robots = []

    with open(filename) as lines:
        for line in lines:
            p_x, p_y, v_x, v_y = rgx.match(line).group(1, 2, 3, 4)
            robots.append([int(p_x), int(p_y), int(v_x), int(v_y)])

    iteration = 0

    # We'll print out anything xmas tree-y and inspect manually to determine if it's a tree
    while True:
        should_print = False

        # Check if we have a row with more than 10 adjacent robots as that may indicate base of a xmas tree
        robot_tuples = sorted([(robot[0], robot[1]) for robot in robots])

        prev_x = -1
        prev_y = -1
        adjacent = 0

        for robot in robot_tuples:
            x = robot[0]
            y = robot[1]

            if x == prev_x and y == prev_y + 1:
                adjacent += 1
            else:
                adjacent = 0

            if adjacent >= 10:
                should_print = True

            prev_x = x
            prev_y = y

        # We're only printing if we think there might be an xmas tree
        if should_print:
            print(iteration)

            for y in range(0, room_height):
                for x in range(0, room_width):
                    if any([robot[0] == x and robot[1] == y for robot in robots]):
                        print("x", end="")
                    else:
                        print(".", end="")
                print("\n")

            print("------------------------------")

            time.sleep(0.5)

        # Iterate the robots
        for i in range(0, len(robots)):
            robots[i][0] = (robots[i][0] + (robots[i][2] * iterations)) % room_width
            robots[i][1] = (robots[i][1] + (robots[i][3] * iterations)) % room_height

        iteration += 1

    return 0


def test_solution_2024_14_A():
    assert solution_2024_14_A("./2024_14/test_input.txt") == 21  # Replace with expected output for the test case


def test_final_solution_2024_14_A():
    assert solution_2024_14_A("./2024_14/input.txt") == 218619324  # Replace with solution when known


# def test_solution_2024_14_B():
#    assert solution_2024_14_B("./2024_14/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_14_B():
#    assert solution_2024_14_B('./2024_14/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_14", sys.argv[1], solution_2024_14_A, solution_2024_14_B)
