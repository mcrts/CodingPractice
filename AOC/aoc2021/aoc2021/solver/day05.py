from collections import Counter
from functools import reduce
import itertools as it
import re
import numpy as np
from typing import Iterator, Self, Tuple
from pydantic import BaseModel

from aoc2021.utils import Solver, input_path


DAY = 5
INPATH = input_path(DAY)

RE_PARSER = r"^(?P<x1>\d+),(?P<y1>\d+)\s->\s(?P<x2>\d+),(?P<y2>\d+)$"


class Position(BaseModel, frozen=True):
    x: int
    y: int

    @classmethod
    def inbetween_positions(cls, p1: Self, p2: Self) -> list[Self]:
        vd = (p2.x - p1.x, p2.y - p1.y)
        p = p1
        s = set([p1, p2])
        while p != p2:
            match vd:
                case (_, 0):
                    p = cls(x=p.x + np.sign(vd[0]), y=p.y)
                case (0, _):
                    p = cls(x=p.x, y=p.y + np.sign(vd[1]))
                case (_, _):
                    p = cls(x=p.x + np.sign(vd[0]), y=p.y + np.sign(vd[1]))
                case _:
                    continue
            s.add(p)

        return list(s)

    @classmethod
    def are_horizontaly_aligned(cls, p1: Self, p2: Self) -> bool:
        return p1.x == p2.x or p1.y == p2.y

    @classmethod
    def are_diagonally_aligned(cls, p1: Self, p2: Self) -> bool:
        return abs(p2.x - p1.x) == abs(p2.y - p1.y)

    @classmethod
    def are_aligned(cls, p1: Self, p2: Self) -> bool:
        return cls.are_horizontaly_aligned(p1, p2) or cls.are_diagonally_aligned(p1, p2)


def parse_input(instream: Iterator[str]) -> Iterator[Tuple[Position, Position]]:
    def filter_parse(s: str) -> bool:
        return bool(re.match(RE_PARSER, s))

    def parse(s: str) -> Tuple[Position, Position]:
        m = re.match(RE_PARSER, s)
        p1 = Position(x=m.group("x1"), y=m.group("y1"))  # type: ignore
        p2 = Position(x=m.group("x2"), y=m.group("y2"))  # type: ignore
        return p1, p2

    stream = filter(filter_parse, instream)
    stream = map(parse, stream)
    return stream


def solve_part1(instream: Iterator[Tuple[Position, Position]]) -> int:
    positions = filter(lambda p: Position.are_horizontaly_aligned(p[0], p[1]), instream)
    positions = it.starmap(Position.inbetween_positions, positions)
    positions = reduce(list.__add__, positions)
    counter = Counter(positions)
    counter2 = Counter({k: v for k, v in counter.items() if v >= 2})
    return len(counter2.keys())


def solve_part2(instream: Iterator[Tuple[Position, Position]]) -> int:
    positions = filter(lambda p: Position.are_aligned(p[0], p[1]), instream)
    positions = it.starmap(Position.inbetween_positions, positions)
    positions = reduce(list.__add__, positions)
    counter = Counter(positions)
    counter2 = Counter({k: v for k, v in counter.items() if v >= 2})
    return len(counter2.keys())


solver01 = Solver(
    parser=parse_input,  # type: ignore
    solver=solve_part1,  # type: ignore
)

solver02 = Solver(
    parser=parse_input,  # type: ignore
    solver=solve_part2,  # type: ignore
)


def main():
    print(f"Day {DAY:02d} - Part01 :", solver01.solve(INPATH))
    print(f"Day {DAY:02d} - Part02 :", solver02.solve(INPATH))
