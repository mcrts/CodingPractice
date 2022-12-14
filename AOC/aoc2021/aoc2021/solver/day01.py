from typing import Iterable, Iterator, Sequence
import itertools as it

from aoc2021.utils import Solver, input_path, T

DAY = 1
INPATH = input_path(DAY)


def nwise(stream: Iterable[T], n) -> Iterator[Sequence[T]]:
    streams = it.tee(stream, n)
    s = it.starmap(lambda i, s: it.islice(s, i, None), enumerate(streams))
    return zip(*s)


def count_successive_value_increase(stream: Iterable[int]) -> int:
    s = it.pairwise(stream)
    s = it.starmap(lambda x1, x2: x1 < x2, s)
    return sum(s)


def count_successive_value_increase_with_sliding_window(stream: Iterable[int]) -> int:
    sliding_window = nwise(stream, 3)
    s = map(sum, sliding_window)
    return count_successive_value_increase(s)


solver01 = Solver(
    parser=lambda s: map(int, s),  # type: ignore
    solver=count_successive_value_increase,  # type: ignore
)

solver02 = Solver(
    parser=lambda s: map(int, s),  # type: ignore
    solver=count_successive_value_increase_with_sliding_window,  # type: ignore
)


def main():
    print(f"Day {DAY:02d} - Part01 :", solver01.solve(INPATH))
    print(f"Day {DAY:02d} - Part02 :", solver02.solve(INPATH))
