import os
from pathlib import Path
from aoc2021.main import AOC_MODULES

DIR_PATH = os.path.dirname(__file__)


def get_input_path(day: int) -> Path:
    return Path(DIR_PATH) / "inputs" / f"day{day:02d}.txt"


def test_day01_part01():
    day = 1
    m = AOC_MODULES[day]
    path = get_input_path(day)
    assert m.solver01.solve(path) == 7


def test_day01_part02():
    day = 1
    m = AOC_MODULES[day]
    path = get_input_path(day)
    assert m.solver02.solve(path) == 5


def test_day06_part01():
    day = 6
    m = AOC_MODULES[day]
    path = get_input_path(day)
    assert m.solver01.solve(path) == 5934


def test_day06_part02():
    day = 6
    m = AOC_MODULES[day]
    path = get_input_path(day)
    assert m.solver02.solve(path) == 26984457539
