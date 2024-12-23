from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x},{self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return self.x < other.x


def get_neighbours(point: Point, width: int, height: int) -> list[Point]:
    above, below, right, left = (None, None, None, None)
    if point.x > 0 and point.x < width and point.y >= 0 and point.y < height:
        left = Point(point.x - 1, point.y)
    if point.x >= 0 and point.x < (width - 1) and point.y >= 0 and point.y < height:
        right = Point(point.x + 1, point.y)
    if point.x >= 0 and point.x < width and point.y > 0 and point.y < height:
        above = Point(point.x, point.y - 1)
    if point.x >= 0 and point.x < width and point.y >= 0 and point.y < (height - 1):
        below = Point(point.x, point.y + 1)
    return [point for point in [left, right, above, below] if point is not None]


def test_get_neighbours():
    assert get_neighbours(Point(0, 0), 1, 1) == []
    assert get_neighbours(Point(0, 0), 2, 2) == [Point(1, 0), Point(0, 1)]
    assert get_neighbours(Point(1, 0), 2, 2) == [Point(0, 0), Point(1, 1)]
    assert get_neighbours(Point(1, 1), 2, 2) == [Point(0, 1), Point(1, 0)]
    assert get_neighbours(Point(0, 1), 2, 2) == [Point(1, 1), Point(0, 0)]


def min_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


@dataclass
class Cell:
    point: Point
    val: str

    def __str__(self):
        return self.val[0:1]


class Grid:
    def __init__(self, vals: list[list[str]]):
        # copy so we don't end up with a ref to some other list
        self.vals = list([list(row) for row in vals])
        self.val_points = defaultdict(list)
        for y, row in enumerate(self.vals):
            for x, val in enumerate(row):
                val_list = self.val_points[val]
                val_list.append(Point(x, y))
                self.val_points[val] = val_list

    def width(self):
        return len(self.vals[0]) if len(self.vals) > 0 else 0

    def height(self):
        return len(self.vals)

    def find_points_with_val(self, val: str) -> list[Point]:
        return self.val_points[val]

    def find_point_with_val(self, val: str) -> Point:
        return self.find_points_with_val(val)[0]

    def set(self, point: Point, val: str):
        self.vals[point.y][point.x] = val

    def get_all_neighbours(self, point: Point):
        above, below, right, left = (None, None, None, None)
        above_point = Point(point.x, point.y - 1)
        above_val = self.val(above_point)
        if above_val != "OUT_OF_BOUNDS":
            above = Cell(above_point, above_val)
        below_point = Point(point.x, point.y + 1)
        below_val = self.val(below_point)
        if below_val != "OUT_OF_BOUNDS":
            below = Cell(below_point, below_val)
        left_point = Point(point.x - 1, point.y)
        left_val = self.val(left_point)
        if left_val != "OUT_OF_BOUNDS":
            left = Cell(left_point, left_val)
        right_point = Point(point.x + 1, point.y)
        right_val = self.val(right_point)
        if right_val != "OUT_OF_BOUNDS":
            right = Cell(right_point, right_val)
        return [above, below, left, right]

    def get_neighbours(self, point: Point):
        return [cell for cell in self.get_all_neighbours(point) if cell is not None]

    def set_val(self, point: Point, value: str):
        if point.x >= 0 and point.x < self.width() and point.y >= 0 and point.y < self.height():
            self.vals[point.y][point.x] = value
        else:
            raise f"Can't set value outside grid {point}"

    def val(self, point: Point) -> str:
        if point.x >= 0 and point.x < self.width() and point.y >= 0 and point.y < self.height():
            return self.vals[point.y][point.x]
        else:
            return "OUT_OF_BOUNDS"

    def val_rows(self) -> list[list[str]]:
        return list([list(row) for row in self.vals])

    def val_cols(self) -> list[list[str]]:
        grid_width = self.width()
        if grid_width > 0:
            cols = []
            for i in range(0, grid_width):
                cols.append([row[i] for row in self.val_rows()])
            return cols
        else:
            return []

    def val_lr_diags(self) -> list[list[str]]:
        grid_width = self.width()
        grid_height = self.width()
        if grid_width > 0 and grid_height > 0:
            diags = []
            for y in range(grid_height - 1, -1, -1):
                diag = []
                x = 0
                while y < grid_height and x < grid_width:
                    diag.append(self.vals[y][x])
                    y += 1
                    x += 1
                diags.append(diag)
            for x in range(1, grid_width):
                diag = []
                y = 0
                while y < grid_height and x < grid_width:
                    diag.append(self.vals[y][x])
                    y += 1
                    x += 1
                diags.append(diag)

            return diags
        else:
            return []

    def val_rl_diags(self) -> list[list[str]]:
        grid_width = self.width()
        grid_height = self.width()
        if grid_width > 0 and grid_height > 0:
            diags = []
            for y in range(grid_height - 1, -1, -1):
                diag = []
                x = grid_width - 1
                while y < grid_height and x >= 0:
                    diag.append(self.vals[y][x])
                    y += 1
                    x -= 1
                diags.append(diag)
            for x in range(grid_width - 2, -1, -1):
                diag = []
                y = 0
                while y < grid_height and x >= 0:
                    diag.append(self.vals[y][x])
                    y += 1
                    x -= 1
                diags.append(diag)
            return diags
        else:
            return []

    def __iter__(self):
        for y, row in enumerate(self.vals):
            for x, val in enumerate(row):
                yield Cell(Point(x, y), val)

    def __str__(self):
        return "\n".join(["".join(row) for row in self.vals])

    def __hash__(self):
        return hash(self.__str__())


def grid_from_lines(lines: list[str]) -> Grid:
    vals = []
    for line in lines:
        vals.append(list(line.strip()))
    return Grid(vals)
