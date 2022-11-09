from collections import Counter
import functools
import os
import itertools as it
from pathlib import Path
from typing import Callable, Iterable, Sequence, Tuple

from aoc2021.utils import T, input_path, Solver

INPATH = input_path(3)


def most_common_bits(instream: Iterable[Sequence[T]]) -> Sequence[T]:
    stream = map(lambda s: tuple(map(lambda x: Counter([x]), s)), instream)
    res = functools.reduce(
        lambda x, y: tuple(i[0] + i[1] for i in zip(x, y)),
        stream,
    )
    res = tuple(map(lambda c: c.most_common(1)[0][0], res))
    return res


def oxygen_critera(instream: Iterable[str]) -> str:
    c = Counter(instream)
    if c["0"] == c["1"]:
        return "1"
    else:
        return c.most_common(1)[0][0]


def co2_criteria(instream: Iterable[str]) -> str:
    c = Counter(instream)
    if c["0"] == c["1"]:
        return "0"
    else:
        return c.most_common()[-1][0]


def compute_bit_criteria(
    instream: Iterable[Sequence[str]], at: int, criteria: Callable
) -> str:
    stream = map(lambda t: t[at], instream)
    return criteria(stream)


def oxygen_generator_rating(instream: Iterable[Sequence[str]]) -> int:
    stream, _instream = it.tee(instream, 2)
    bits = ""
    for i in range(12):
        stream, _instream = it.tee(_instream, 2)
        stream = filter(lambda s: "".join(s).startswith(bits), stream)
        bits += compute_bit_criteria(stream, i, oxygen_critera)

    rating = int(bits, 2)
    return rating


def co2_scrubber_rating(instream: Iterable[Sequence[str]]) -> int:
    stream, _instream = it.tee(instream, 2)
    bits = ""
    for i in range(12):
        stream, _instream = it.tee(_instream, 2)
        stream = filter(lambda s: "".join(s).startswith(bits), stream)
        bits += compute_bit_criteria(stream, i, co2_criteria)
    rating = int(bits, base=2)
    return rating


def solve_part1(instream: Iterable[Sequence[str]]) -> int:
    base = int("0b111111111111", base=0)
    gamma_bits = "".join(most_common_bits(instream))
    gamma_rate = int(gamma_bits, 2)
    epsilon_rate = base ^ gamma_rate
    return gamma_rate * epsilon_rate


def solve_part2(instream: Iterable[Sequence[str]]) -> int:
    s1, s2 = it.tee(instream, 2)
    r1 = oxygen_generator_rating(s1)
    r2 = co2_scrubber_rating(s2)
    return r1 * r2


def parse_input(instream: Iterable[str]) -> Iterable[Sequence[str]]:
    return map(lambda s: tuple(s), instream)


solver01 = Solver(
    parser=parse_input,  # type: ignore
    solver=solve_part1,  # type: ignore
)

solver02 = Solver(
    parser=parse_input,  # type: ignore
    solver=solve_part2,  # type: ignore
)


def main():
    print("Day 03 - Part01 :", solver01.solve(INPATH))
    print("Day 03 - Part02 :", solver02.solve(INPATH))
