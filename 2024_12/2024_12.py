import sys
from common.utils import run
from common.grid import grid_from_lines


def solution_2024_12_A(filename: str) -> int:
    with open(filename) as file:
        lines = list(file)
    farm = grid_from_lines(lines)
    visited = set()
    total_fence_cost = 0
    for plot in farm:
        plant = plot.val
        if plot.point not in visited:
            stack = [plot.point]
            region = set()
            perimeter = 0
            while stack:
                cur_plot = stack.pop()
                if cur_plot not in region:
                    region.add(cur_plot)
                    visited.add(cur_plot)
                    for neighbour in farm.get_neighbours(cur_plot):
                        if neighbour.val == plant and neighbour.point not in visited:
                            stack.append(neighbour.point)
                        elif neighbour.val != plant:
                            perimeter += 1
                    if cur_plot.x == 0 or cur_plot.x == (farm.width() - 1):
                        perimeter += 1
                    if cur_plot.y == 0 or cur_plot.y == (farm.height() - 1):
                        perimeter += 1
            fence_cost = len(region) * perimeter
            total_fence_cost += fence_cost
    return total_fence_cost


def solution_2024_12_B(filename: str) -> int:
    return 0


def test_solution_2024_12_A():
    assert solution_2024_12_A("./2024_12/test_input.txt") == 1930  # Replace with expected output for the test case


# def test_final_solution_2024_12_A():
#    assert solution_2024_12_A('./2024_12/input.txt') == 0 # Replace with solution when known


def test_solution_2024_12_B():
    assert solution_2024_12_B("./2024_12/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_2024_12_B():
#    assert solution_2024_12_B('./2024_12/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_12", sys.argv[1], solution_2024_12_A, solution_2024_12_B)
