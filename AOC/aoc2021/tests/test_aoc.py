import os
from pathlib import Path

import pytest
from aoc2021.main import SOLVERS

DIR_PATH = os.path.dirname(__file__)


def get_input_path(day: int) -> Path:
    return Path(DIR_PATH) / "inputs" / f"day{day:02d}.txt"


SOLUTIONS = {
    (1, 1): 7,
    (1, 2): 5,
    (2, 1): 150,
    (2, 2): 900,
    (3, 1): 198,
    (3, 2): 230,
    (4, 1): 4512,
    (4, 2): 1924,
    (5, 1): 5,
    (5, 2): 12,
    (6, 1): 5934,
    (6, 2): 26984457539,
    (7, 1): 37,
    (7, 2): 168,
    (8, 1): None,
    (8, 2): None,
}


@pytest.mark.parametrize("day", set([k[0] for k in SOLUTIONS.keys()]))
def test_testfile_exists(day):
    assert get_input_path(day).exists(), f"test file for day{day:02d} does not exist."


@pytest.mark.parametrize("day", set([k[0] for k in SOLUTIONS.keys()]))
def test_testfile_has_content(day):
    if get_input_path(day).exists():
        with open(get_input_path(day), "r") as f:
            content = f.read()
    else:
        content = ""
    assert content, f"test file for day{day:02d} is empty."


@pytest.mark.parametrize("day, part", SOLUTIONS.keys())
def test_day(day: int, part: int):
    solver = SOLVERS[(day, part)]  # type: ignore
    path = get_input_path(day)
    assert solver.solve(path) == SOLUTIONS[(day, part)]  # type: ignore
