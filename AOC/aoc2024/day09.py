import functools as F
from collections import namedtuple
from enum import IntEnum, auto
from pprint import pprint
from typing import Iterable, Tuple


def expand(report: Iterable[int]) -> list[str]:
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


def part01(pipe: Iterable[str]) -> int:
    report = list(map(int, next(pipe).strip()))
    report = expand(report)
    report = compress_frag(report)

    count = 0
    for i, v in enumerate(report):
        if v != ".":
            count += i * int(v)
    return count


from collections import namedtuple

Empty = namedtuple("Empty", [])
Buffering = namedtuple("Buffering", ["key", "size"])


def move(report: list[str], idx: int, buffer: Buffering):
    subreport = report[0:idx]

    groups = (
        subreport[i : i + buffer.size] for i in range(len(subreport) - buffer.size + 1)
    )
    groups = (i for i, g in enumerate(groups) if "".join(g) == "." * buffer.size)
    groups = list(groups)
    if groups:
        new_idx = groups[0]
        for i in range(buffer.size):
            report[new_idx + i] = buffer.key
            report[idx + i] = "."


def part02(pipe: Iterable[str]) -> int:
    report = list(map(int, next(pipe).strip()))
    report = expand(report)

    new_report = list(report)
    state = Empty()
    j = len(report) - 1
    while j >= 0:
        match state, report[j]:
            case Empty(), ".":
                j -= 1
            case Empty(), k:
                state = Buffering(key=k, size=1)
                j -= 1
            case Buffering(key=k, size=s), ".":
                move(new_report, j + 1, state)
                state = Empty()
                j -= 1
            case Buffering(key=k, size=s), v:
                if k == v:
                    state = Buffering(key=k, size=s + 1)
                else:
                    move(new_report, j + 1, state)
                    state = Buffering(key=v, size=1)
                j -= 1

    count = 0
    for i, v in enumerate(new_report):
        if v != ".":
            count += i * int(v)
    return count
