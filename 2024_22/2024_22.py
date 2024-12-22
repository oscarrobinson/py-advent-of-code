import sys
from common.utils import run
from collections import defaultdict


def get_nth_secret_number(initial: int, n: int) -> int:
    secret = initial
    for _ in range(0, n):
        step_1 = secret << 6  # multiply 64
        step_2 = step_1 ^ secret  # mix
        step_3 = step_2 % 16777216  # prune (16777216 is 2^24 so may be a more efficient modulo somehow)
        step_4 = step_3 >> 5  # divide 32
        step_5 = step_4 ^ step_3  # mix
        step_6 = step_5 % 16777216  # prune
        step_7 = step_6 << 11  # multiply 2048
        step_8 = step_7 ^ step_6  # mix
        secret = step_8 % 16777216  # prune
    return secret


def secret_number_to_price(secret: int) -> int:
    return secret % 10


def solution_2024_22_A(filename: str) -> int:
    total = 0
    with open(filename) as lines:
        for line in lines:
            initial = int(line.strip())
            total += get_nth_secret_number(initial, 2000)
    return total


def solution_2024_22_B(filename: str) -> int:
    seq_totals = defaultdict(lambda: 0)

    with open(filename) as lines:
        for line in lines:
            initial = int(line.strip())
            price_sequence = []
            last_price = secret_number_to_price(initial)
            last_secret = initial
            # Price you get first time each sequence appears
            this_monkey_seq_prices = {}
            for i in range(1, 2001):
                cur_secret = get_nth_secret_number(last_secret, 1)
                cur_price = secret_number_to_price(cur_secret)
                diff = cur_price - last_price
                price_sequence.append(diff)
                # Trim the sequence once we get more than last 4 diffs
                if len(price_sequence) == 5:
                    price_sequence = price_sequence[1:5]
                # Add current price to our total for each sequence type
                if len(price_sequence) == 4:
                    sequence = (price_sequence[0], price_sequence[1], price_sequence[2], price_sequence[3])
                    if sequence not in this_monkey_seq_prices:
                        this_monkey_seq_prices[sequence] = cur_price
                last_price = cur_price
                last_secret = cur_secret

            for seq, price in this_monkey_seq_prices.items():
                seq_totals[seq] += price

    return max([price for price in seq_totals.values()])


def test_solution_2024_22_A():
    assert solution_2024_22_A("./2024_22/test_input.txt") == 37327623  # Replace with expected output for the test case


# def test_final_solution_2024_22_A():
#    assert solution_2024_22_A('./2024_22/input.txt') == 0 # Replace with solution when known


def test_solution_2024_22_B():
    assert solution_2024_22_B("./2024_22/test_input_2.txt") == 23  # Replace with expected output for the test case


# def test_final_solution_2024_22_B():
#    assert solution_2024_22_B('./2024_22/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_22", sys.argv[1], solution_2024_22_A, solution_2024_22_B)
