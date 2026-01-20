from typing import Iterator, Self, Tuple
from dataclasses import dataclass
import re

from enum import StrEnum


class State(StrEnum):
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Action:
    state: State
    value: int

    RE_TOKEN: str = r"(L|R)(\d+)"

    @classmethod
    def from_line(cls, line: str) -> Self:
        m = re.match(cls.RE_TOKEN, line)
        if not m:
            raise ValueError("Failed to parse string", line)

        s, d = m.groups()
        return cls(State(s), int(d))

    def compress(self, base=100) -> Tuple[int, Self]:
        n = self.value // base
        a = type(self)(self.state, self.value % base)
        return (n, a)


@dataclass
class Lock:
    number: int = 50
    counter: int = 0
    base: int = 100

    def add(self, v: int):
        self.number += v
        self.number = self.number % self.base
        if self.number == 0:
            self.counter += 1

    def move(self, a: Action):
        n, a = a.compress()
        self.counter += n

        match a:
            case Action(State.LEFT, d):
                for _ in range(d):
                    self.decrement()
            case Action(State.RIGHT, d):
                for _ in range(d):
                    self.increment()

    def increment(self):
        self.add(1)

    def decrement(self):
        self.add(-1)


def part1(pipe: Iterator[str]):
    lock = Lock()
    actions = [Action.from_line(line) for line in pipe]
    for a in actions:
        match a:
            case Action(State.LEFT, d):
                lock.add(-d)
            case Action(State.RIGHT, d):
                lock.add(d)
    return lock.counter


def part2(pipe: Iterator[str]):
    lock = Lock()
    actions = [Action.from_line(line) for line in pipe]
    for a in actions:
        lock.move(a)
    return lock.counter
