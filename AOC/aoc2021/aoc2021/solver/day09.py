from typing import Iterator, Any, Sequence, Tuple, TypeVar, NamedTuple
import itertools as it
import numpy as np

from aoc2021.utils import Solver, input_path

DAY = 9
INPATH = input_path(DAY)

Index = Tuple[int, int]
Point = NamedTuple(
    "Point", [("index", Index), ("heatmap", np.ndarray), ("height", int)]
)


def parser(instream: Iterator[Sequence[int]]) -> np.ndarray:
    it_array = (np.array(s, dtype=int) for s in instream)
    arr = np.vstack(list(it_array))
    return arr


def solver_part01(input_var: np.ndarray) -> int:
    def is_low_point(x: int, others: Sequence[int]) -> bool:
        return all(map(lambda i: i - x > 0, others))

    def adjacency_generator(arr: np.ndarray) -> Iterator[Tuple[int, Sequence[int]]]:
        index_deltas = set([(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)]) - set(
            [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        )
        indexes = set(np.ndindex(arr.shape))
        for index, x in np.ndenumerate(arr):
            neighbours = ((index[0] + d[0], index[1] + d[1]) for d in index_deltas)
            neighbours = (i for i in neighbours if i in indexes)
            yield (x, [arr[n] for n in neighbours])

    low_points = [e[0] + 1 for e in adjacency_generator(input_var) if is_low_point(*e)]
    return sum(low_points)


def solver_part02(input_var: Any) -> int:
    return 0


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
