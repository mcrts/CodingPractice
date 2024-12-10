import functools as F
from collections import namedtuple
from enum import IntEnum, auto
from pprint import pprint
from typing import Iterable, Tuple


def expand(report: Iterable[int]) -> Iterable[str]:
    blockid = 0
    expanded_report = []
    is_file = True
    for i in report:
        if is_file:
            expanded_report.extend([str(blockid)] * i)
            blockid += 1
        else:
            expanded_report.extend(["."] * i)
        is_file = not is_file
    return expanded_report


def compress_frag(report: Iterable[str]) -> Iterable[str]:
    r = list(report)
    i = 0
    j = len(r) - 1
    while i < j:
        if r[i] != ".":
            i += 1
        elif r[j] == ".":
            j -= 1
        else:
            r[i], r[j] = r[j], r[i]
            i += 1
            j -= 1
    return r


def part1(pipe: Iterable[str]) -> int:
    report = list(map(int, next(pipe).strip()))
    report = expand(report)
    report = compress_frag(report)

    count = 0
    for i, v in enumerate(report):
        if v != ".":
            count += i * int(v)
    return count


def expand2(report: Iterable[int]) -> list[Tuple[str, int]]:
    blockid = 0
    expanded_report = []
    is_file = True
    for i in report:
        if is_file:
            expanded_report.extend([(str(blockid), i)] * i)
            blockid += 1
        else:
            expanded_report.extend([(".", i)] * i)
        is_file = not is_file
    return expanded_report


def compress(report: list[Tuple[str, int]]) -> list[str]:
    r = list(report)
    i = 0
    j = len(r)

    while j > 0:
        bid, length = r[j - 1]
        if bid != ".":
            free_offsets = [
                idx
                for idx, (b, l) in enumerate(report)
                if b == "." and l >= length and idx < j - length
            ]
            if free_offsets:
                i = free_offsets[0]
                s0 = r[:i]
                s1 = r[i : i + length]
                s2 = r[i + length : j - length]
                s3 = r[j - length : j]
                s4 = r[j:]
                r = s0 + s3 + s2 + s1 + s4

    return r


def part2(pipe: Iterable[str]) -> int:
    report = list(map(int, next(pipe).strip()))
    report = expand2(report)

    # pprint(report)
    report = compress(report)
    pprint(report)

    return 0
