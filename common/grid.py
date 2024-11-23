from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x},{self.y})"


def min_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


@dataclass
class Cell:
    point: Point
    val: str

    def __str__(self):
        return self.val


class Grid:
    def __init__(self, vals: list[list[str]]):
        # copy so we don't end up with a ref to some other list
        self.vals = list([list(row) for row in vals])

    def width(self):
        return len(self.vals[0]) if len(self.vals) > 0 else 0

    def height(self):
        return len(self.vals)

    def val_rows(self):
        return list([list(row) for row in self.vals])

    def val_cols(self):
        grid_width = self.width()
        if grid_width > 0:
            cols = []
            for i in range(0, grid_width):
                cols.append([row[i] for row in self.val_rows()])
            return cols
        else:
            return []

    def __iter__(self):
        for y, row in enumerate(self.vals):
            for x, val in enumerate(row):
                yield Cell(Point(x, y), val)

    def __str__(self):
        return "\n".join(["".join(row) for row in self.vals])


def grid_from_lines(lines: list[str]) -> Grid:
    vals = []
    for line in lines:
        vals.append(list(line.strip()))
    return Grid(vals)
