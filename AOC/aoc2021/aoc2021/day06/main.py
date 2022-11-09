import os
from pathlib import Path
from typing import Iterator, Sequence, Tuple
from functools import cache

from aoc2021.utils import Solver

DIR_PATH = os.path.dirname(__file__)
INPATH = Path(DIR_PATH) / "input.txt"
DAY = "06"


def parser(instream: Iterator[str]) -> list[int]:
    fishes = list(map(int, next(instream).split(",")))
    return fishes


def true_adult_lifespan(fishes: list[int], n: int) -> list[int]:
    return [n + 6 - f for f in fishes]


@cache
def fish_fertility(f: int) -> Tuple[int, int]:
    return (f, f // 7)


@cache
def generation(fish: Tuple[int, int]) -> Sequence[int]:
    generation, childs = fish
    return tuple([generation - 7 * i - 2 for i in range(1, childs + 1)])


@cache
def fish_reproduce(f: int) -> Sequence[int]:
    fishes = generation(fish_fertility(f))
    return fishes


@cache
def fish_childs(f: int) -> int:
    childs = fish_reproduce(f)
    counter = 1
    for c in childs:
        counter += fish_childs(c)
    return counter


def solver(input_var: list[int], n: int) -> int:
    fishes = input_var
    fishes = true_adult_lifespan(fishes, n)
    c = sum(fish_childs(f) for f in fishes)
    return c


solver01 = Solver(
    parser=parser,  # type: ignore
    solver=lambda x: solver(x, 80),  # type: ignore
)

solver02 = Solver(
    parser=parser,  # type: ignore
    solver=lambda x: solver(x, 256),  # type: ignore
)


def main():
    print(f"Day {DAY} - Part01 :", solver01.solve(INPATH))
    print(f"Day {DAY} - Part02 :", solver02.solve(INPATH))
