import sys
import time
from common.utils import run
from common.grid import grid_from_lines, Grid, Point

ROBOT = "@"
EMPTY = "."
BOX = "O"
UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"
WALL = "#"
BOX_LEFT = "["
BOX_RIGHT = "]"


def move(warehouse: Grid, cur_loc: Point, direction: str):
    if direction == UP:
        mov_to_loc = Point(cur_loc.x, cur_loc.y - 1)
    elif direction == RIGHT:
        mov_to_loc = Point(cur_loc.x + 1, cur_loc.y)
    elif direction == DOWN:
        mov_to_loc = Point(cur_loc.x, cur_loc.y + 1)
    elif direction == LEFT:
        mov_to_loc = Point(cur_loc.x - 1, cur_loc.y)

    if warehouse.val(mov_to_loc) == EMPTY:
        item_val = warehouse.val(cur_loc)
        warehouse.set_val(cur_loc, EMPTY)
        warehouse.set_val(mov_to_loc, item_val)
        return mov_to_loc
    elif warehouse.val(mov_to_loc) == WALL:
        return cur_loc
    elif warehouse.val(mov_to_loc) == BOX:
        box_new_loc = move(warehouse, mov_to_loc, direction)
        if box_new_loc != mov_to_loc:
            item_val = warehouse.val(cur_loc)
            warehouse.set_val(cur_loc, EMPTY)
            warehouse.set_val(mov_to_loc, item_val)
            return mov_to_loc
        else:
            return cur_loc


def get_opposite(direction: str) -> str:
    if direction == UP:
        return DOWN
    elif direction == DOWN:
        return UP
    elif direction == LEFT:
        return RIGHT
    elif direction == RIGHT:
        return LEFT


def can_move_wide(warehouse: Grid, cur_loc, direction: str):
    if direction == UP:
        mov_to_loc = Point(cur_loc.x, cur_loc.y - 1)
    elif direction == RIGHT:
        mov_to_loc = Point(cur_loc.x + 1, cur_loc.y)
    elif direction == DOWN:
        mov_to_loc = Point(cur_loc.x, cur_loc.y + 1)
    elif direction == LEFT:
        mov_to_loc = Point(cur_loc.x - 1, cur_loc.y)

    if warehouse.val(mov_to_loc) == EMPTY:
        return True
    elif warehouse.val(mov_to_loc) == WALL:
        return False
    elif (warehouse.val(mov_to_loc) == BOX_LEFT or warehouse.val(mov_to_loc) == BOX_RIGHT) and direction in ["<", ">"]:
        return can_move_wide(warehouse, mov_to_loc, direction)
    elif warehouse.val(mov_to_loc) == BOX_LEFT and direction in ["^", "v"]:
        box_left_loc = mov_to_loc
        box_right_loc = Point(mov_to_loc.x + 1, mov_to_loc.y)
        return can_move_wide(warehouse, box_left_loc, direction) and can_move_wide(warehouse, box_right_loc, direction)
    elif warehouse.val(mov_to_loc) == BOX_RIGHT and direction in ["^", "v"]:
        box_left_loc = Point(mov_to_loc.x - 1, mov_to_loc.y)
        box_right_loc = mov_to_loc
        return can_move_wide(warehouse, box_left_loc, direction) and can_move_wide(warehouse, box_right_loc, direction)


def move_wide(warehouse: Grid, cur_loc: Point, direction: str):
    if direction == UP:
        mov_to_loc = Point(cur_loc.x, cur_loc.y - 1)
    elif direction == RIGHT:
        mov_to_loc = Point(cur_loc.x + 1, cur_loc.y)
    elif direction == DOWN:
        mov_to_loc = Point(cur_loc.x, cur_loc.y + 1)
    elif direction == LEFT:
        mov_to_loc = Point(cur_loc.x - 1, cur_loc.y)

    if warehouse.val(mov_to_loc) == EMPTY:
        item_val = warehouse.val(cur_loc)
        warehouse.set_val(cur_loc, EMPTY)
        warehouse.set_val(mov_to_loc, item_val)
        return mov_to_loc
    elif warehouse.val(mov_to_loc) == WALL:
        return cur_loc
    elif (warehouse.val(mov_to_loc) == BOX_LEFT or warehouse.val(mov_to_loc) == BOX_RIGHT) and direction in ["<", ">"]:
        box_new_loc = move_wide(warehouse, mov_to_loc, direction)
        if box_new_loc != mov_to_loc:
            item_val = warehouse.val(cur_loc)
            warehouse.set_val(cur_loc, EMPTY)
            warehouse.set_val(mov_to_loc, item_val)
            return mov_to_loc
        else:
            return cur_loc
    elif (warehouse.val(mov_to_loc) == BOX_RIGHT or warehouse.val(mov_to_loc) == BOX_LEFT) and direction in ["^", "v"]:
        box_left_loc = Point(mov_to_loc.x - 1, mov_to_loc.y) if warehouse.val(mov_to_loc) == BOX_RIGHT else mov_to_loc
        box_right_loc = Point(mov_to_loc.x + 1, mov_to_loc.y) if warehouse.val(mov_to_loc) == BOX_LEFT else mov_to_loc
        if can_move_wide(warehouse, box_left_loc, direction) and can_move_wide(warehouse, box_right_loc, direction):
            move_wide(warehouse, box_left_loc, direction)
            move_wide(warehouse, box_right_loc, direction)
            item_val = warehouse.val(cur_loc)
            warehouse.set_val(cur_loc, EMPTY)
            warehouse.set_val(mov_to_loc, item_val)
            return mov_to_loc
        else:
            return cur_loc


# fmt: off
def test_move_wide():
    warehouse = grid_from_lines([
        "########",
        "##.@..##",
        "##[]..##",
        "##.[].##",
        "##[]..##",
        "########"
    ])
    robot_pos = get_robot_pos(warehouse)
    move_wide(warehouse, robot_pos, DOWN)

    expected = [
        "########",
        "##.@..##",
        "##[]..##",
        "##.[].##",
        "##[]..##",
        "########"
    ]

    assert str(warehouse) == "\n".join(expected)

def test_move_wide_with_naughty_obstacle():
    warehouse = grid_from_lines([
        "########",
        "##.@..##",
        "##[]..##",
        "###[].##",
        "##....##",
        "########"
    ])
    robot_pos = get_robot_pos(warehouse)
    move_wide(warehouse, robot_pos, DOWN)

    expected = [
        "########",
        "##.@..##",
        "##[]..##",
        "###[].##",
        "##....##",
        "########"
    ]

    assert str(warehouse) == "\n".join(expected)
# fmt: on


def parse_grid_and_movement_lines(filename) -> (list[str], list[str]):
    grid_lines = []
    mov_lines = []
    with open(filename) as lines:
        for line in lines:
            if UP in line or DOWN in line or LEFT in line or RIGHT in line:
                mov_lines.append(line)
            elif line != "\n":
                grid_lines.append(line)

    return (grid_lines, mov_lines)


def movements_from_mov_lines(mov_lines: list[str]) -> list[str]:
    return [instr for line in mov_lines for instr in line if instr != "\n"]


def get_warehouse(grid_lines: list[str]) -> Grid:
    return grid_from_lines(grid_lines)


def get_wide_warehouse(grid_lines: list[str]) -> Grid:
    expanded_grid_lines = []
    for line in grid_lines:
        items = []
        for item in line:
            if item != "\n":
                if item == BOX:
                    items.append(BOX_LEFT)
                    items.append(BOX_RIGHT)
                elif item == ROBOT:
                    items.append(ROBOT)
                    items.append(EMPTY)
                else:
                    items.append(item)
                    items.append(item)
        expanded_grid_lines.append("".join(items))
    return grid_from_lines(expanded_grid_lines)


def get_robot_pos(warehouse: Grid) -> Point:
    return [cell for cell in warehouse if cell.val == ROBOT][0].point


def sum_coords_for_item(warehouse: Grid, item: str) -> int:
    result = 0
    for pos in warehouse:
        if pos.val == item:
            result += pos.point.x + (pos.point.y * 100)

    return result


def solution_2024_15_A(filename: str) -> int:
    grid_lines, mov_lines = parse_grid_and_movement_lines(filename)

    warehouse = get_warehouse(grid_lines)
    movements = movements_from_mov_lines(mov_lines)
    robot_pos = get_robot_pos(warehouse)

    for movement in movements:
        robot_pos = move(warehouse, robot_pos, movement)

    return sum_coords_for_item(warehouse, BOX)


def print_warehouse(warehouse):
    returns = "\r".join(["\033[A" for _ in range(0, warehouse.height() - 1)]) + "\r"
    print(warehouse, end=returns, flush=True)
    time.sleep(0.0025)


def solution_2024_15_B(filename: str) -> int:
    grid_lines, mov_lines = parse_grid_and_movement_lines(filename)
    movements = movements_from_mov_lines(mov_lines)
    warehouse = get_wide_warehouse(grid_lines)
    robot_pos = get_robot_pos(warehouse)

    for movement in movements:
        robot_pos = move_wide(warehouse, robot_pos, movement)
        # print_warehouse(warehouse)

    return sum_coords_for_item(warehouse, BOX_LEFT)


def test_solution_2024_15_A():
    assert solution_2024_15_A("./2024_15/test_input.txt") == 10092  # Replace with expected output for the test case


def test_final_solution_2024_15_A():
    assert solution_2024_15_A("./2024_15/input.txt") == 1509863  # Replace with solution when known


def test_solution_2024_15_B():
    assert solution_2024_15_B("./2024_15/test_input.txt") == 9021  # Replace with expected output for the test case


def test_final_solution_2024_15_B():
    assert solution_2024_15_B("./2024_15/input.txt") == 1548815  # Replace with solution when known


if __name__ == "__main__":
    run("2024_15", sys.argv[1], solution_2024_15_A, solution_2024_15_B)
