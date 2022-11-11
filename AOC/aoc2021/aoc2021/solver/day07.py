from typing import Iterator, Sequence, Callable
from functools import cache

from aoc2021.utils import Solver, input_path


DAY = 7
INPATH = input_path(DAY)


def parser(instream: Iterator[str]) -> Sequence[int]:
    line = next(instream)
    return list(map(int, line.split(",")))


@cache
def base_cost(pos: int, new_pos: int) -> int:
    return abs(pos - new_pos)


def cost_fun(crabs: Sequence[int], pos: int) -> int:
    return sum(map(lambda x: base_cost(x, pos), crabs))


@cache
def sustained_cost(pos: int, new_pos: int) -> int:
    return sum(range(1, base_cost(pos, new_pos) + 1))


def sustained_cost_fun(crabs: Sequence[int], pos: int) -> int:
    return sum(map(lambda x: sustained_cost(x, pos), crabs))


def optimal(
    crabs: Sequence[int], cost_function: Callable[[Sequence[int], int], int]
) -> int:
    cost = cost_function(crabs, 0)
    for i in range(1, max(crabs) + 1):
        c = cost_function(crabs, i)
        if c < cost:
            cost = c
        else:
            break
    return cost


def solver_part01(crabs: Sequence[int]) -> int:
    return optimal(
        crabs,
        cost_fun,
    )


def solver_part02(crabs: Sequence[int]) -> int:
    return optimal(
        crabs,
        sustained_cost_fun,
    )


solver01 = Solver(
    parser=parser,  # type: ignore
    solver=solver_part01,  # type: ignore
)

solver02 = Solver(
    parser=parser,  # type: ignore
    solver=solver_part02,  # type: ignore
)


def main():
    print(f"Day {DAY:02d} - Part01 :", solver01.solve(INPATH))
    print(f"Day {DAY:02d} - Part02 :", solver02.solve(INPATH))
