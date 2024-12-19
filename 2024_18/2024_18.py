import sys
import heapq
import time
from common.utils import run
from common.grid import Point, get_neighbours, min_distance


def debug_print(drop_locations, grid_size, open_points, closed_points):
    to_print_lines = [f"open points: {len(open_points)}", f"closed points: {len(closed_points)}"]
    open_points = set([p for _, _, p in open_points])
    closed_points = set([p for _, p in closed_points])
    for x in range(0, grid_size + 1):
        to_print_row = []
        for y in range(0, grid_size + 1):
            if Point(x, y) in drop_locations:
                to_print_row.append("#")
            elif Point(x, y) in open_points:
                to_print_row.append("?")
            elif Point(x, y) in closed_points:
                to_print_row.append("O")
            else:
                to_print_row.append(".")
        to_print_lines.append("".join(to_print_row))

    to_print = "\n".join(to_print_lines)
    end = "\r".join(["\033[A" for _ in range(0, len(to_print_lines) - 1)]) + "\r"

    print(to_print, end=end, flush=True)

    time.sleep(0.01)


def solution_2024_18_A(filename: str, grid_size: int = 70, bytes_fallen: int = 1024) -> int:
    all_drop_locations = []

    with open(filename) as lines:
        for line in lines:
            x, y = [int(num.strip()) for num in line.split(",")]
            all_drop_locations.append(Point(x, y))

    drop_locations = set(all_drop_locations[0:bytes_fallen])

    goal = Point(grid_size, grid_size)

    open_points = []
    heapq.heapify(open_points)
    closed_points = set()
    heapq.heappush(open_points, (0, 0, Point(0, 0)))

    # A* Search for shortest path
    while open_points:
        q_f, q_g, q = heapq.heappop(open_points)
        successors = get_neighbours(q, grid_size + 1, grid_size + 1)
        for s in successors:
            if s == goal:
                return q_g + 1
            elif s not in drop_locations:
                s_g = q_g + 1
                s_h = min_distance(s, goal)
                s_f = s_g + s_h
                should_skip = False

                for p_f, _, p in open_points:
                    if p == s and p_f <= s_f:
                        should_skip = True
                        break

                for p_f, p in closed_points:
                    if p == s and p_f <= s_f:
                        should_skip = True
                        break

                if not should_skip:
                    heapq.heappush(open_points, (s_f, s_g, s))
            closed_points.add((q_f, q))


def is_path(drop_locations: list[Point], goal: Point) -> bool:
    stack = [Point(0, 0)]
    visited = set()

    while stack:
        loc = stack.pop()
        if loc == goal:
            return True
        visited.add(loc)
        neighbours = get_neighbours(loc, goal.x + 1, goal.y + 1)
        for neighbour in neighbours:
            if neighbour not in drop_locations and neighbour not in visited:
                stack.append(neighbour)
    return False


#                                               start at 1024 cos we know there's a path still from part A
def solution_2024_18_B(filename: str, grid_size: int = 70, start_at=1024) -> int:
    all_drop_locations = []

    with open(filename) as lines:
        for line in lines:
            x, y = [int(num.strip()) for num in line.split(",")]
            all_drop_locations.append(Point(x, y))
    # coudld make this binary search to speed it up a bit but I'm too lazy
    for i in range(start_at, len(all_drop_locations)):
        print(i)
        if not is_path(all_drop_locations[0 : i + 1], Point(grid_size, grid_size)):
            return f"{all_drop_locations[i].x},{all_drop_locations[i].y}"

    return ""


def test_solution_2024_18_A():
    assert (
        solution_2024_18_A("./2024_18/test_input.txt", grid_size=6, bytes_fallen=12) == 22
    )  # Replace with expected output for the test case


# def test_final_solution_2024_18_A():
#    assert solution_2024_18_A('./2024_18/input.txt') == 0 # Replace with solution when known


def test_solution_2024_18_B():
    assert (
        solution_2024_18_B("./2024_18/test_input.txt", grid_size=6, start_at=0) == "6,1"
    )  # Replace with expected output for the test case


# def test_final_solution_2024_18_B():
#    assert solution_2024_18_B('./2024_18/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_18", sys.argv[1], solution_2024_18_A, solution_2024_18_B)
