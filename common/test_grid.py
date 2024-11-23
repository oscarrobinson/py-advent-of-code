from common.grid import Grid, Cell, Point, grid_from_lines


def test_grid_not_ref_to_passed_list():
    original_list = [["a", "b"], ["c", "d"]]
    grid = Grid(original_list)
    original_list[0][0] = "x"
    assert original_list[0][0] == "x"
    assert grid.val_rows()[0][0] == "a"


def test_grid_width():
    assert grid_from_lines(["ab", "cd"]).width() == 2


def test_empty_grid_width():
    assert grid_from_lines([]).width() == 0


def test_grid_iterator():
    raw_grid = ["ab", "cd"]
    grid = grid_from_lines(raw_grid)
    assert list(grid) == [
        Cell(Point(0, 0), "a"),
        Cell(Point(1, 0), "b"),
        Cell(Point(0, 1), "c"),
        Cell(Point(1, 1), "d"),
    ]


def test_grid_val_cols():
    raw_grid = ["ab", "cd"]
    grid = grid_from_lines(raw_grid)
    assert grid.val_cols() == [["a", "c"], ["b", "d"]]
