import time
from typing import Callable
from typing import Optional


def ns_to_duration_str(ns: int) -> str:
    seconds = ns / 1_000_000_000
    return f"{seconds:.6f}s"


def run(
    name: str, problem: Optional[str], implementation_a: Callable[[str], int], implementation_b: Callable[[str], int]
) -> None:
    if problem == "A":
        implementation = implementation_a
    elif problem == "B":
        implementation = implementation_b
    else:
        raise ValueError("Invalid problem, specify A or B")

    t_start = time.time_ns()
    solution = implementation(f"{name}/input.txt")
    t_elapsed = time.time_ns() - t_start
    print(f"Solution to {name}-{problem} (Computed in {ns_to_duration_str(t_elapsed)}): {solution}")
