import time
import re
from common.utils import run


class GameSet:
    def __init__(self, raw: str):
        self.r = self.get_colour('red', raw)
        self.b = self.get_colour('blue', raw)
        self.g = self.get_colour('green', raw)

    def get_colour(self, col: str, raw: str) -> int:
        result = re.search(r'([0-9]+) '+col, raw)
        if result:
            return int(result.group(1))
        else:
            return 0

class Game:
    def __init__(self, raw: str):
        games_raw = raw.split(':')[1]
        self.id = int(raw.split(':')[0][5:])
        raw_sets = games_raw.split(';')
        self.sets = [GameSet(raw_set) for raw_set in raw_sets]

    def possible(self, r: int, g: int, b: int) -> bool:
        for game_set in self.sets:
            if game_set.r > r or game_set.g > g or game_set.b > b:
                return False
        return True

    def min_required_cubes(self):
        r = 0
        b = 0
        g = 0

        for game_set in self.sets:
            r = max([r, game_set.r])
            g = max([g, game_set.g])
            b = max([b, game_set.b])

        return {'r': r, 'g': g, 'b': b}

    def min_required_cubes_powerset(self) -> int:
        mins = self.min_required_cubes()
        return mins['r'] * mins['g'] * mins['b']

def get_games(filename: str) -> list[Game]:
     with open(filename) as input:
        return [Game(line) for line in input]

def solution_2023_02_A(filename: str) -> int:
    games = get_games(filename)
    result = 0
    for game in games:
        if game.possible(12, 13, 14):
            result += game.id
    return result

def solution_2023_02_B(filename: str) -> int:
    games = get_games(filename)
    result = 0
    for game in games:
        result += game.min_required_cubes_powerset()
    return result

def test_min_required_cubes():
    assert Game('Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green').min_required_cubes() == {'r': 4, 'g': 2, 'b': 6}
    assert Game('Game 7: 3 green, 2 blue; 1 green, 1 blue').min_required_cubes() == {'r': 0, 'b': 2, 'g': 3}

def test_game_is_possible():
    assert Game('Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red').possible(r=12, g=13, b=14) == False
    assert Game('Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green').possible(r=12, g=13, b=14) == True

def test_game_id():
    assert Game('Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red').id == 3

def test_parsing_of_game_sets():
    game_set = GameSet(' 3 blue, 4 red   ')
    assert game_set.r == 4
    assert game_set.b == 3
    assert game_set.g == 0

def test_solution_2023_02_A():
    assert solution_2023_02_A('./2023_02/test_input.txt') == 8 # Replace with expected output for the test case

def test_final_solution_2023_02_A():
    assert solution_2023_02_A('./2023_02/input.txt') == 2600

def test_solution_2023_02_B():
    assert solution_2023_02_B('./2023_02/test_input.txt') == 2286 # Replace with expected output for the test case

def test_final_solution_2023_02_B():
    assert solution_2023_02_B('./2023_02/input.txt') == 86036

if __name__ == '__main__':
    run('2023_02_A', solution_2023_02_A)
    run('2023_02_B', solution_2023_02_B)
    