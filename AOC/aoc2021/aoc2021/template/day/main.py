import os
from pathlib import Path
from typing import Iterator, Any
import itertools as it

from aoc2021.utils import Solver

DIR_PATH = os.path.dirname(__file__)
INPATH = Path(DIR_PATH) / "input.txt"
DAY = "01"


def parser_part01(instream: Iterator[str]) -> Any:
    return 0


def parser_part02(instream: Iterator[str]) -> Any:
    return 0


def solver_part01(input_var: Any) -> int:
    return 0


def solver_part02(input_var: Any) -> int:
    return 0


solver01 = Solver(
    parser=parser_part01,  # type: ignore
    solver=solver_part01,  # type: ignore
)

solver02 = Solver(
    parser=parser_part02,  # type: ignore
    solver=solver_part02,  # type: ignore
)


def main():
    print(f"Day {DAY} - Part01 :", solver01.solve(INPATH))
    print(f"Day {DAY} - Part02 :", solver02.solve(INPATH))
