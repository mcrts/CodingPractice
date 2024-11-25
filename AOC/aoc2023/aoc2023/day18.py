import functools as F
import itertools as I
import re
import sys
from collections import namedtuple
from enum import Enum
from pprint import pprint
from typing import Any, Iterable, List, Mapping, NamedTuple, Optional, Set, Tuple

import numpy as np


class Direction(Enum):
    U = "U"
    R = "R"
    D = "D"
    L = "L"


Direction.OFFSETS = {
    Direction.U: (-1, 0),
    Direction.R: (0, 1),
    Direction.D: (1, 0),
    Direction.L: (0, -1),
}


class Instruction(NamedTuple):
    d: Direction
    count: int
    rgb: str

    @classmethod
    def fromLine(cls, line: str):
        d, x, rgb = line.strip().split(" ")
        rgb = rgb[2:-1]
        return cls(Direction(d), int(x), rgb)


class Position(NamedTuple):
    x: int
    y: int


def process_instruction(start: Position, ins: Instruction) -> Tuple[Position, Iterable[Position]]:
    dx, dy = Direction.OFFSETS[ins.d]
    dugged = [Position(start.x + (i + 1) * dx, start.y + (i + 1) * dy) for i in range(ins.count)]
    return dugged[-1], dugged


def part1(pipe):
    s0 = Position(0, 0)
    dugged = set()
    for l in pipe:
        instruction = Instruction.fromLine(l)
        s0, positions = process_instruction(s0, instruction)
        dugged = dugged | set(positions)
    xmin, ymin = 0, 0
    xmax = max(dugged, key=lambda p: p.x)
    ymax = max(dugged, key=lambda p: p.y)

    g = np.empty((xmax, ymax))
    return 0


def part2(pipe):
    for l in pipe:
        print(l.strip())
    return 0
