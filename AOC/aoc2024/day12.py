import itertools as I
import sys
from pprint import pprint
from typing import Iterator, NamedTuple, Tuple

import numpy as np


class Coordinate2D(NamedTuple):
    x: int
    y: int

    def touch(self, p) -> bool:
        d = abs(self.x - p.x) + abs(self.y - p.y)
        return d <= 1

    def neighbours(self) -> set:
        points = set()
        points.add(Coordinate2D(self.x - 1, self.y))
        points.add(Coordinate2D(self.x + 1, self.y))
        points.add(Coordinate2D(self.x, self.y - 1))
        points.add(Coordinate2D(self.x, self.y + 1))
        return points


def get_children(p: Coordinate2D, xmin: int, xmax: int, ymin: int, ymax: int) -> list:
    children = p.neighbours()
    children = [c for c in children if xmin <= c.x < xmax and ymin <= c.y < ymax]
    return children


class Region(NamedTuple):
    label: str
    points: set[Coordinate2D]

    def touch(self, p: Coordinate2D) -> bool:
        return any(n.touch(p) for n in self.points)

    def cost(self) -> int:
        area = len(self.points)
        perimeter = 0
        for p in self.points:
            perimeter += len(p.neighbours() - self.points)
        return area, perimeter


def discover_region(grid: np.ndarray, label: str, p: Coordinate2D) -> Region:
    points = set()
    xmax, ymax = grid.shape
    frontier = [p]
    visited = set([p])
    while frontier:
        n = frontier.pop(0)
        visited.add(n)
        if grid[n] == label:
            points.add(n)
            children = get_children(n, xmin=0, xmax=xmax, ymin=0, ymax=ymax)
            frontier.extend(set(children) - visited)

    return Region(label=label, points=points)


def parse_input(pipe: Iterator[str]) -> dict[str, Region]:
    arr = []
    for l in pipe:
        arr.append(list(l.strip()))
    grid = np.array(arr)

    regions: dict[str, list[Region]] = dict()
    visited: set[Coordinate2D] = set()
    for i, v in np.ndenumerate(grid):
        v = str(v)
        p = Coordinate2D(x=i[0], y=i[1])
        if p in visited:
            continue

        print(p)
        if v not in regions.keys():
            r = discover_region(grid, label=v, p=p)
            regions[v] = [r]
            visited = visited | r.points
        elif p not in visited:
            r = discover_region(grid, label=v, p=p)
            regions[v].append(r)
            visited = visited | r.points
        else:
            visited.add(p)

    return regions


def part01(pipe: Iterator[str]):
    regions = parse_input(pipe)
    result = 0
    for k, v in regions.items():
        for r in v:
            area, perimeter = r.cost()
            cost = area * perimeter
            result += cost
    return result


def part02(pipe: Iterator[str]):
    return 0
