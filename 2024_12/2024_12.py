import sys
from common.utils import run
from common.grid import grid_from_lines, Point


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
    with open(filename) as file:
        lines = list(file)
    farm = grid_from_lines(lines)
    visited = set()
    total_fence_cost = 0

    regions = []

    for plot in farm:
        plant = plot.val
        if plot.point not in visited:
            stack = [plot.point]
            region = set()
            while stack:
                cur_plot = stack.pop()
                if cur_plot not in region:
                    region.add(cur_plot)
                    visited.add(cur_plot)
                    for neighbour in farm.get_neighbours(cur_plot):
                        if neighbour.val == plant and neighbour.point not in visited:
                            stack.append(neighbour.point)
            regions.append(region)

    for region in regions:
        # Sort by x coord then y coord order so are walking points by column in order
        column_order = sorted(region, key=lambda p: (p.x, p.y))
        prev_point = None
        on_side = False
        sides = 0
        # Check the left side of every point
        for point in column_order:
            # If already on a side, check if we're still on the same side
            if on_side:
                # no longer on same side if point to direct left is in same region we haven't taken a contiguous step down
                if farm.val(point) == farm.val(Point(point.x-1, point.y)) or point.y != prev_point.y+1:
                    on_side = False
                    sides += 1

            # If not already on a side/no longer on a side, check if we're on a new side
            if not on_side:
                # on a side if point to the direct left is out of bounds or a different plant
                if farm.val(point) != farm.val(Point(point.x-1, point.y)):
                    on_side = True

            prev_point = point
        
        # Check if our final point counts as a side
        if on_side:
            sides += 1

        prev_point = None
        on_side = False

        # Check the right side of every point
        for point in column_order:
            # If already on a side, check if we're still on the same side
            if on_side:
                # no longer on same side if point to direct right is in same region we haven't taken a contiguous step down
                if farm.val(point) == farm.val(Point(point.x+1, point.y)) or point.y != prev_point.y+1:
                    on_side = False
                    sides += 1

            # If not already on a side/no longer on a side, check if we're on a new side
            if not on_side:
                # on a side if point to the direct right is out of bounds or a different plant
                if farm.val(point) != farm.val(Point(point.x+1, point.y)):
                    on_side = True

            prev_point = point

        # Check if our final point counts as a side
        if on_side:
            sides += 1

        prev_point = None
        on_side = False

        # Sort by y coord then x coord order so are walking points by row in order
        row_order = sorted(region, key=lambda p: (p.y, p.x))
        prev_point = None
        on_side = False
        # Check the top side of every point
        for point in row_order:

            # If already on a side, check if we're still on the same side
            if on_side:
                # no longer on same side if point to direct above is in same region we haven't taken a contiguous step right
                if farm.val(point) == farm.val(Point(point.x, point.y-1)) or point.x != prev_point.x+1:
                    on_side = False
                    sides += 1

            # If not already on a side/no longer on a side, check if we're on a new side
            if not on_side:
                # on a side if point to the direct above is out of bounds or a different plant
                if farm.val(point) != farm.val(Point(point.x, point.y-1)):
                    on_side = True

            prev_point = point
        
        # Check if our final point counts as a side
        if on_side:
            sides += 1

        prev_point = None
        on_side = False

        # Check the below side of every point
        for point in row_order:
            # If already on a side, check if we're still on the same side
            if on_side:
                # no longer on same side if point to direct right is in same region we haven't taken a contiguous step right
                if farm.val(point) == farm.val(Point(point.x, point.y+1)) or point.x != prev_point.x+1:
                    on_side = False
                    sides += 1

            # If not already on a side/no longer on a side, check if we're on a new side
            if not on_side:
                # on a side if point direct below is out of bounds or a different plant
                if farm.val(point) != farm.val(Point(point.x, point.y+1)):
                    on_side = True

            prev_point = point

        # Check if our final point counts as a side
        if on_side:
            sides += 1

        total_fence_cost += len(region) * sides
    return total_fence_cost


def test_solution_2024_12_A():
    assert solution_2024_12_A("./2024_12/test_input.txt") == 1930  # Replace with expected output for the test case


# def test_final_solution_2024_12_A():
#    assert solution_2024_12_A('./2024_12/input.txt') == 0 # Replace with solution when known


def test_solution_2024_12_B():
    assert solution_2024_12_B("./2024_12/test_input.txt") == 1206  # Replace with expected output for the test case


# def test_final_solution_2024_12_B():
#    assert solution_2024_12_B('./2024_12/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_12", sys.argv[1], solution_2024_12_A, solution_2024_12_B)
