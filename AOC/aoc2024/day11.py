import functools as F
import itertools as I
import math as M
from collections import namedtuple
from enum import IntEnum, auto
from pprint import pprint
from typing import Iterable, Tuple


@F.lru_cache()
def update_once(v: str) -> Tuple[str, ...]:
    match v, len(v) % 2 == 0:
        case "0", _:
            return ("1",)
        case _, True:
            m = len(v) // 2
            a = v[:m]
            b = v[m:].lstrip("0")
            if b:
                return (a, b)
            else:
                return (a,)
        case _:
            return (str(int(v) * 2024),)


@F.lru_cache()
def update_once(v: int) -> Tuple[int, ...]:
    n = len(str(v))
    match v, n % 2 == 0:
        case 0, _:
            return (1,)
        case _, True:
            m = n // 2
            a = v // 10**m
            b = v % 10**m
            return (a, b)
        case _:
            return (v * 2024,)


def count(v: int, n: int) -> int:
    if n == 0:
        return 1
    elif n > 0:
        arr = update_once(v)
        return count_array(arr, n - 1)


def count_array(arr: list[int], n: int) -> int:
    return sum([count(a, n) for a in arr])


def part1(pipe: Iterable[str]) -> int:
    arr = list(map(int, next(pipe).strip().split(" ")))
    for _ in range(25):
        arr = list(I.chain.from_iterable([update_once(n) for n in arr]))
    return len(arr)


def part2(pipe: Iterable[str]) -> int:
    arr = list(map(int, next(pipe).strip().split(" ")))
    return count_array(arr, 75)
