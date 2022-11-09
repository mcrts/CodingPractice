import os
from pathlib import Path

import pytest
from aoc2021.main import AOC_MODULES, DAYS_IMPLEMENTED

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
}


@pytest.mark.parametrize("part", (1, 2))
@pytest.mark.parametrize("day", range(1, DAYS_IMPLEMENTED + 1))
def test_day(day: int, part: int):
    m = AOC_MODULES[day]
    path = get_input_path(day)
    match part:
        case 1:
            solver = m.solver01
        case 2:
            solver = m.solver02

    assert solver.solve(path) == SOLUTIONS[(day, part)]  # type: ignore
