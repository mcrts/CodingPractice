from functools import reduce, cache
from typing import Counter, Iterator, Any, Optional, Sequence, Tuple, NamedTuple
import itertools as it
import numpy as np
from dataclasses import dataclass

from aoc2021.utils import Solver, input_path

DAY = 9
INPATH = input_path(DAY)


@dataclass(frozen=True)
class Heatmap(np.ndarray):
    pass


Index = Tuple[int, int]
Point = NamedTuple("Point", [("index", Index), ("heatmap", Heatmap), ("height", int)])


def get_neighbours(p: Point) -> Sequence[Point]:
    index_deltas = set([(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)]) - set(
        [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    )
    indexes = set(np.ndindex(p.heatmap.shape))
    neighbours = ((p.index[0] + d[0], p.index[1] + d[1]) for d in index_deltas)
    neighbours = (Point(i, p.heatmap, p.heatmap[i]) for i in neighbours if i in indexes)
    return list(neighbours)


@cache
def is_low_point(p: Point) -> bool:
    neighbours = get_neighbours(p)
    relative_height = [(n.height - p.height) > 0 for n in neighbours]
    return all(relative_height)


@cache
def find_basin(p: Point) -> Optional[Index]:
    if p.height == 9:
        return None
    if is_low_point(p):
        return p.index
    else:
        n = min(get_neighbours(p), key=lambda p: p.height)
        return find_basin(n)


def parser(instream: Iterator[Sequence[int]]) -> Heatmap:
    it_array = (np.array(s, dtype=int) for s in instream)
    arr = np.vstack(list(it_array))
    heatmap = arr.view(Heatmap)
    return heatmap


def solver_part01(heatmap: Heatmap) -> int:
    points = (Point(i, heatmap, h) for i, h in np.ndenumerate(heatmap))
    lowpoints = filter(is_low_point, points)
    return sum([p.height + 1 for p in lowpoints])


def solver_part02(heatmap: Heatmap) -> int:
    points = (Point(i, heatmap, h) for i, h in np.ndenumerate(heatmap))
    coloredmap = filter(lambda i: i is not None, map(find_basin, points))
    counter = Counter(coloredmap)
    return reduce(int.__mul__, map(lambda x: x[1], counter.most_common(3)))


solver01 = Solver(
    lineparser=list,
    parser=parser,  # type: ignore
    solver=solver_part01,  # type: ignore
)

solver02 = Solver(
    lineparser=list,
    parser=parser,  # type: ignore
    solver=solver_part02,  # type: ignore
)


def main():
    print(f"Day {DAY:02d} - Part01 :", solver01.solve(INPATH))
    print(f"Day {DAY:02d} - Part02 :", solver02.solve(INPATH))
