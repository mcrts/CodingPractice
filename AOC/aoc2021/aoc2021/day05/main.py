from collections import Counter
from functools import reduce
import itertools as it
import os
import re
import numpy as np
from pathlib import Path
from typing import Iterator, Self, Tuple

from pydantic import BaseModel

from aoc2021.utils import stream_from_text

DIR_PATH = os.path.dirname(__file__)
INPATH = Path(DIR_PATH) / "input.txt"
DAY = "05"

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


def solve_part1(instream: Iterator[str]) -> int:
    stream = parse_input(instream)
    positions = filter(lambda p: Position.are_horizontaly_aligned(p[0], p[1]), stream)
    positions = it.starmap(Position.inbetween_positions, positions)
    positions = reduce(list.__add__, positions)
    counter = Counter(positions)
    counter2 = Counter({k: v for k, v in counter.items() if v >= 2})
    return len(counter2.keys())


def solve_part2(instream: Iterator[str]) -> int:
    stream = parse_input(instream)
    positions = filter(lambda p: Position.are_aligned(p[0], p[1]), stream)
    positions = it.starmap(Position.inbetween_positions, positions)
    positions = reduce(list.__add__, positions)
    counter = Counter(positions)
    counter2 = Counter({k: v for k, v in counter.items() if v >= 2})
    return len(counter2.keys())


def main():
    stream = stream_from_text(INPATH)
    print(
        f"Day {DAY} - Part01 : {solve_part1(stream)}",
    )

    stream = stream_from_text(INPATH)
    print(
        f"Day {DAY} - Part02 : {solve_part2(stream)}",
    )
