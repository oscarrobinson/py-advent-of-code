import sys
from common.utils import run
from common.grid import grid_from_lines, Grid, Cell, Point

poss_guards = ["<", ">", "^", "v"]


def get_guard_pos(guard_map: Grid) -> Cell:
    for pos in guard_map:
        if pos.val in poss_guards:
            return pos
    return None


def get_guard_vel(guard: Cell) -> (int, int):
    if guard.val == "^":
        return (0, -1)
    elif guard.val == ">":
        return (1, 0)
    elif guard.val == "v":
        return (0, 1)
    elif guard.val == "<":
        return (-1, 0)


def rotate_guard(guard: Cell) -> Cell:
    if guard.val == "^":
        return Cell(point=guard.point, val=">")
    elif guard.val == ">":
        return Cell(point=guard.point, val="v")
    elif guard.val == "v":
        return Cell(point=guard.point, val="<")
    elif guard.val == "<":
        return Cell(point=guard.point, val="^")


def guard_on_map(guard: Cell, guard_map: Grid) -> bool:
    width = guard_map.width()
    height = guard_map.height()
    g_x = guard.point.x
    g_y = guard.point.y
    return g_x < width and g_x >= 0 and g_y < height and g_y >= 0


def get_points_visited(guard: Cell, guard_map: Grid) -> set[Point]:
    vel_x, vel_y = get_guard_vel(guard)
    pos_visited = set()

    while guard_on_map(guard, guard_map):
        pos_visited.add((guard.point.x, guard.point.y))
        next_point = Point(guard.point.x + vel_x, guard.point.y + vel_y)
        if guard_map.val(next_point) == "#":
            guard = rotate_guard(guard)
            vel_x, vel_y = get_guard_vel(guard)
        else:
            guard = Cell(next_point, guard.val)
    return pos_visited


def solution_2024_06_A(filename: str) -> int:
    with open(filename) as lines:
        guard_map = grid_from_lines(list(lines))
    guard = get_guard_pos(guard_map)
    return len(get_points_visited(guard, guard_map))


def solution_2024_06_B(filename: str) -> int:
    with open(filename) as lines:
        lines = list(lines)
    guard_map = grid_from_lines(lines)
    guard = get_guard_pos(guard_map)
    points_visited = get_points_visited(guard, guard_map)
    poss_positions = len(points_visited)
    pos_considered = 0
    result = 0
    # We'll try and put an obstacle at every point in the guard's path
    # We then check if playing the guard's route results in a cycle
    for x, y in points_visited:
        point = Point(x, y)
        pos_considered += 1
        print(f"{pos_considered}/{poss_positions}")

        guard_map = grid_from_lines(lines)
        guard = get_guard_pos(guard_map)

        if guard_map.val(point) != "#" and guard.point != point:
            guard_map.set(point, "#")
            guard_map.set(guard.point, ".")

            vel_x, vel_y = get_guard_vel(guard)
            pos_visited_at_vel = set()

            while guard_on_map(guard, guard_map):
                next_point = Point(guard.point.x + vel_x, guard.point.y + vel_y)
                if guard_map.val(next_point) == "#":
                    guard = rotate_guard(guard)
                    vel_x, vel_y = get_guard_vel(guard)
                else:
                    guard = Cell(next_point, guard.val)
                    pos_and_vel = (guard.point.x, guard.point.y, vel_x, vel_y)

                    loop_detected = pos_and_vel in pos_visited_at_vel

                    if loop_detected:
                        result += 1
                        break
                    pos_visited_at_vel.add(pos_and_vel)

    return result


def test_solution_2024_06_A():
    assert solution_2024_06_A("./2024_06/test_input.txt") == 41  # Replace with expected output for the test case


def test_final_solution_2024_06_A():
    assert solution_2024_06_A("./2024_06/input.txt") == 4964  # Replace with solution when known


def test_solution_2024_06_B():
    assert solution_2024_06_B("./2024_06/test_input.txt") == 6  # Replace with expected output for the test case


# def test_final_solution_2024_06_B():
#    assert solution_2024_06_B('./2024_06/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_06", sys.argv[1], solution_2024_06_A, solution_2024_06_B)
