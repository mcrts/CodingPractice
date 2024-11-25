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


class Point(NamedTuple):
    x: int
    y: int


class Geometric:
    @classmethod
    def segment_intersects(cls, a: Point, b: Point, c: Point, d: Point) -> bool:
        alpha = a.x - b.x
        beta = a.y - b.y
        gamma = c.x - d.x
        delta = c.y - d.y
        denom = (alpha * delta) - (beta * gamma)
        if denom == 0:
            return False
        else:
            t = ((a.x - c.x) * delta - (a.y - c.y) * gamma) / denom
            u = -(alpha * (a.y - c.y) - beta * (a.x - c.x)) / denom
            return (0 < t <= 1) and (0 < u <= 1)


class Segment(NamedTuple):
    p0: Point
    p1: Point

    @classmethod
    def _intersects(cls, l1, l2) -> bool:
        return Geometric.segment_intersects(l1.p0, l1.p1, l2.p0, l2.p1)

    def intersects(self, other) -> bool:
        return self._intersects(self, other)


class Polygon(NamedTuple):
    points: set[Point]
    segments: List[Segment]

    def bounding_box(self) -> Tuple[int, int, int, int]:
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return min(xs), max(xs), min(ys), max(ys)

    def is_in(self, p: Point) -> bool:
        if p in self.points:
            return True
        else:
            l = Segment(Point(p.x, -1), p)
            count = sum(s.intersects(l) for s in self.segments)
            return (count % 2) == 1


def process_instruction(start: Point, ins: Instruction) -> Tuple[Point, Iterable[Point]]:
    dx, dy = Direction.OFFSETS[ins.d]
    dugged = [Point(start.x + (i + 1) * dx, start.y + (i + 1) * dy) for i in range(ins.count)]
    return dugged[-1], dugged


def part1(pipe):
    p0 = Point(0, 0)
    dugged = set()
    segments = []
    for l in pipe:
        instruction = Instruction.fromLine(l)
        p1, positions = process_instruction(p0, instruction)
        segments.append(Segment(p0, p1))
        dugged = dugged | set(positions)
        p0 = p1

    polygon = Polygon(points=dugged, segments=segments)
    x0, x1, y0, y1 = polygon.bounding_box()
    arr = [[polygon.is_in(Point(x, y)) for y in range(0, y1 + 1)] for x in range(0, x1 + 1)]
    grid = np.array(arr)
    return grid.sum()


def part2(pipe):
    for l in pipe:
        print(l.strip())
    return 0
