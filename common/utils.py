import time
from typing import Callable

def ns_to_duration_str(ns: int) -> str:
    seconds = ns / 1_000_000_000
    return f"{seconds:.6f}s"

def run(name: str, implementation: Callable[[str], int]) -> None:
    t_start = time.time_ns()
    solution = implementation('input.txt')
    t_elapsed = time.time_ns() - t_start
    print(f'Solution to {name} (Computed in {ns_to_duration_str(t_elapsed)}): {solution}')