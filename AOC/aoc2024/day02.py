import itertools as I
import math as M
import sys
from collections import Counter
from typing import Iterator


def is_safe(report):
    delta = tuple(I.starmap(int.__sub__, zip(report[0:-1], report[1:])))
    c = Counter(delta)
    is_all_positive = all(map(lambda v: v > 0, c.keys()))
    is_all_negative = all(map(lambda v: v < 0, c.keys()))
    is_within_range = all(tuple(map(lambda v: 0 < abs(v) < 4, c.keys())))

    return is_within_range and (is_all_positive or is_all_negative)


def is_safe_dampened(report):
    for i in range(len(report)):
        r = list(report)
        r.pop(i)
        if is_safe(r):
            return True

    return False


def part01(pipe: Iterator[str]):
    reports = []
    for l in pipe:
        r = tuple(map(int, l.strip().split(" ")))
        reports.append(r)

    count = 0
    for r in reports:
        if is_safe(r):
            count += 1
    return count


def part02(pipe: Iterator[str]):
    reports = []
    for l in pipe:
        r = tuple(map(int, l.strip().split(" ")))
        reports.append(r)

    count = 0
    for r in reports:
        flag = is_safe(r)
        if not flag:
            flag = is_safe_dampened(r)

        if flag:
            count += 1

    return count
