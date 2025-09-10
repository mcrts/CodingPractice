import itertools as I
import sys
from pprint import pprint
from typing import Iterator, NamedTuple, Tuple


def int_concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


class Entry(NamedTuple):
    result: int
    values: Tuple[int, ...]

    @classmethod
    def from_str(cls, s: str):
        result, values = s.split(":", 1)
        result = int(result)
        values = tuple(map(int, filter(bool, values.split(" "))))
        return cls(result=result, values=values)

    def test_equation(self, operators):
        values = list(self.values)
        r = values.pop(0)
        for op in operators:
            r = op(r, values.pop(0))
        return r == self.result

    def __bool__(self):
        perm = I.product((int.__mul__, int.__add__), repeat=len(self.values) - 1)
        return any(self.test_equation(p) for p in perm)


class Entry2(NamedTuple):
    result: int
    values: Tuple[int, ...]

    @classmethod
    def from_str(cls, s: str):
        result, values = s.split(":", 1)
        result = int(result)
        values = tuple(map(int, filter(bool, values.split(" "))))
        return cls(result=result, values=values)

    def test_equation(self, operators):
        values = list(self.values)
        r = values.pop(0)
        for op in operators:
            r = op(r, values.pop(0))
        return r == self.result

    def __bool__(self):
        perm = I.product((int.__mul__, int.__add__, int_concat), repeat=len(self.values) - 1)
        return any(self.test_equation(p) for p in perm)


def part01(pipe: Iterator[str]):
    c = 0
    for l in pipe:
        e = Entry.from_str(l.strip())
        if bool(e):
            c += e.result
    return c


def part02(pipe: Iterator[str]):
    c = 0
    for l in pipe:
        e = Entry2.from_str(l.strip())
        if bool(e):
            c += e.result
    return c
