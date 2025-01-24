import itertools as I
import operator
import sys
from collections import defaultdict
from pprint import pprint
from typing import Dict, Iterator, NamedTuple, Set, Tuple

Coordinate2D = Tuple[int, int]


def Coordinate2D_add(a: Coordinate2D, b: Coordinate2D) -> Coordinate2D:
    return tuple(map(operator.add, zip(a, b)))


class Antenna(NamedTuple):
    frequency: str
    coordinate: Coordinate2D


def parse_input(pipe: Iterator[str]) -> Dict[str, Set[Antenna]]:
    s = defaultdict(set)
    for i, l in enumerate(pipe):
        for j, c in enumerate(l.strip()):
            if c != ".":
                s[c].add(Antenna(c, (i, j)))
    return s


def part01(pipe: Iterator[str]):
    antennas = parse_input(pipe)
    print(antennas)
    return 0


def part02(pipe: Iterator[str]):
    return 0
