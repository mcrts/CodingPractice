from typing import Iterator, Self, Tuple
from dataclasses import dataclass
import re

from enum import StrEnum

RE_RANGE = r"(\d+)-(\d+)"


def parse(pipe: Iterator[str]) -> Iterator[re.Match]:
    for s in pipe:
        for m in re.finditer(RE_RANGE, s):
            yield m


def is_valid1(string: str) -> bool:
    l = int(len(string) / 2)
    return not (string[:l] == string[l:])


def is_valid2(string: str) -> bool:
    lmax = int(len(string) / 2)
    for n in range(1, lmax + 1):
        if len(string) % n == 0:
            groups = (string[i : i + n] for i in range(0, len(string), n))
            if len(set(groups)) == 1:
                return False

    return True


def part1(pipe: Iterator[str]):
    res = 0
    for m in parse(pipe):
        id1 = m.group(1)
        id2 = m.group(2)
        for i in range(int(id1), int(id2) + 1):
            if not is_valid1(str(i)):
                res += i

    return res


def part2(pipe: Iterator[str]):
    res = 0
    for m in parse(pipe):
        id1 = m.group(1)
        id2 = m.group(2)
        for i in range(int(id1), int(id2) + 1):
            if not is_valid2(str(i)):
                res += i

    return res
