from collections import Counter
import functools
import itertools as it
from typing import Callable, Iterable, Sequence, Self
from pydantic import BaseModel

from aoc2021.utils import T, input_path, Solver


DAY = 3
INPATH = input_path(DAY)


def partition(pred, iterable):
    "Use a predicate to partition entries into false entries and true entries"
    t1, t2 = it.tee(iterable)
    return it.filterfalse(pred, t1), filter(pred, t2)


class Reading(BaseModel):
    bits: Sequence[str]

    @classmethod
    def fromString(cls, s: str) -> Self:
        bits = list(s)
        return cls(bits=bits)

    def __len__(self) -> int:
        return len(self.bits)

    def read_at(self, i: int) -> str:
        return self.bits[i]


class Device(BaseModel):
    readings: Sequence[Reading]

    @property
    def bit_length(self) -> int:
        return len(self.readings[0])

    def most_common_bit(self, idx: int) -> str:
        bits = map(lambda r: Reading.read_at(r, idx), self.readings)
        c = Counter(bits)
        return c.most_common(1)[0][0]

    def least_common_bit(self, idx: int) -> str:
        bits = map(lambda r: Reading.read_at(r, idx), self.readings)
        c = Counter(bits)
        return c.most_common()[-1][0]

    def gamma_rate(self) -> int:
        bits = [self.most_common_bit(i) for i in range(0, self.bit_length)]
        rate = int("".join(bits), base=2)
        return rate

    def epsilon_rate(self) -> int:
        bits = [self.least_common_bit(i) for i in range(0, self.bit_length)]
        rate = int("".join(bits), base=2)
        return rate

    def o2_rating(self, i: int = 0) -> int:
        if len(self.readings) == 1:
            return int("".join(self.readings[0].bits), base=2)

        readings0, readings1 = partition(lambda x: x.read_at(i) == "1", self.readings)
        readings0 = list(readings0)
        readings1 = list(readings1)
        if len(readings0) > len(readings1):
            return Device(readings=readings0).o2_rating(i + 1)
        else:
            return Device(readings=readings1).o2_rating(i + 1)

    def co2_rating(self, i: int = 0) -> int:
        if len(self.readings) == 1:
            return int("".join(self.readings[0].bits), base=2)

        readings0, readings1 = partition(lambda x: x.read_at(i) == "1", self.readings)
        readings0 = list(readings0)
        readings1 = list(readings1)
        if len(readings0) <= len(readings1):
            return Device(readings=readings0).co2_rating(i + 1)
        else:
            return Device(readings=readings1).co2_rating(i + 1)


def solve_part1(device: Device) -> int:
    return device.gamma_rate() * device.epsilon_rate()


def solve_part2(device: Device) -> int:
    o2_rating = device.o2_rating()
    co2_rating = device.co2_rating()
    return o2_rating * co2_rating


def parse_input(readings: Iterable[Reading]) -> Device:
    return Device(readings=list(readings))


solver01 = Solver(
    lineparser=Reading.fromString,  # type: ignore
    parser=parse_input,  # type: ignore
    solver=solve_part1,  # type: ignore
)

solver02 = Solver(
    lineparser=Reading.fromString,  # type: ignore
    parser=parse_input,  # type: ignore
    solver=solve_part2,  # type: ignore
)


def main():
    print(f"Day {DAY:02d} - Part01 :", solver01.solve(INPATH))
    print(f"Day {DAY:02d} - Part02 :", solver02.solve(INPATH))
