import itertools as I
import operator
import sys
from collections import defaultdict
from pprint import pprint
from typing import Dict, Iterator, NamedTuple, Set, Tuple

Coordinate2D = Tuple[int, int]


def Coordinate2D_add(a: Coordinate2D, b: Coordinate2D) -> Coordinate2D:
    return tuple(map(operator.add, a, b))


def Coordinate2D_sub(a: Coordinate2D, b: Coordinate2D) -> Coordinate2D:
    return tuple(map(operator.sub, a, b))


class Antenna(NamedTuple):
    frequency: str
    coordinate: Coordinate2D

    def antinode(self, other) -> Coordinate2D:
        d = Coordinate2D_sub(other.coordinate, self.coordinate)
        c = Coordinate2D_add(other.coordinate, d)
        return c

    def resonant_antinode(self, other, xmax: int, ymax: int) -> Set[Coordinate2D]:
        antinodes = set()
        for k in I.count(0, step=1):
            d = Coordinate2D_sub(other.coordinate, self.coordinate)
            d = tuple(k * i for i in d)
            c = Coordinate2D_add(other.coordinate, d)
            if 0 <= c[0] <= xmax and 0 <= c[1] <= ymax:
                antinodes.add(c)
            else:
                break
        return antinodes


def parse_input(pipe: Iterator[str]) -> Tuple[Dict[str, Set[Antenna]], int, int]:
    xmax = 0
    ymax = 0
    s = defaultdict(set)
    for i, l in enumerate(pipe):
        xmax = i if i > xmax else xmax
        for j, c in enumerate(l.strip()):
            ymax = j if j > ymax else ymax
            if c != ".":
                s[c].add(Antenna(c, (i, j)))
    return s, xmax, ymax


def part01(pipe: Iterator[str]):
    g_antennas, xmax, ymax = parse_input(pipe)
    antinodes = set()
    for k, antennas in g_antennas.items():
        for a, b in I.permutations(antennas, 2):
            c = a.antinode(b)
            antinodes.add(c)
    antinodes = set(c for c in antinodes if 0 <= c[0] <= xmax and 0 <= c[1] <= ymax)
    return len(antinodes)


def part02(pipe: Iterator[str]):
    g_antennas, xmax, ymax = parse_input(pipe)
    antinodes = set()
    for k, antennas in g_antennas.items():
        for a, b in I.permutations(antennas, 2):
            new_antinodes = a.resonant_antinode(b, xmax, ymax)
            antinodes = antinodes.union(new_antinodes)
    return len(antinodes)
