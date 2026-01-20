import os
from enum import Enum
from pathlib import Path
from typing import NamedTuple

import pytest
import importlib

DIR_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
SRC_PATH = DIR_PATH.parent
TESTFILES = SRC_PATH / "test_files"


class Part(Enum):
    PART1 = 1
    PART2 = 2


class State(NamedTuple):
    day: int
    part: Part
    solution: int


states = [State(1, Part.PART1, 3), State(1, Part.PART2, 6)]


@pytest.mark.parametrize("s", states)
def test(s: State):
    m = importlib.import_module(f"aoc2025.day{s.day:02d}")
    finput = TESTFILES / f"day{s.day:02d}.txt"

    pipe = finput.open("r").readlines()
    match s.part:
        case Part.PART1:
            assert m.part1(pipe) == s.solution
        case Part.PART2:
            assert m.part2(pipe) == s.solution
