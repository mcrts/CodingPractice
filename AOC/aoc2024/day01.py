import functools as F
import itertools as I
import sys
from collections import Counter
from typing import Iterator


def part01(pipe: Iterator[str]):
    left = []
    right = []
    for l in pipe:
        x1, x2 = l.strip().split("   ", 2)
        left.append(int(x1))
        right.append(int(x2))

    left.sort()
    right.sort()
    r = F.reduce(
        int.__add__, map(int.__abs__, I.starmap(int.__sub__, zip(left, right)))
    )
    return r


def part02(pipe: Iterator[str]):
    left = []
    right = []
    for l in pipe:
        x1, x2 = l.strip().split("   ", 2)
        left.append(int(x1))
        right.append(int(x2))

    cleft = Counter(left)
    cright = Counter(right)
    score = 0
    for k, v in cleft.items():
        score += k * cright[k] * v
    return score
