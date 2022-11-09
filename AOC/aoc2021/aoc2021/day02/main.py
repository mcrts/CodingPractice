from collections import Counter, namedtuple
from functools import reduce
import itertools as it
import os
from pathlib import Path
from typing import Dict, Iterable, Tuple, Self

from pydantic import BaseModel, parse_obj_as
from enum import Enum

from aoc2021.utils import Solver, input_path

INPATH = input_path(2)


class MotionEnm(str, Enum):
    forward = "forward"
    up = "up"
    down = "down"


class SubmarineCommand(BaseModel):
    motion: MotionEnm
    units: int


class SubmarineState(BaseModel):
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    def apply_command(self, command: SubmarineCommand) -> Self:
        match command:
            case SubmarineCommand(motion=MotionEnm.up, units=units):
                aim = self.aim - units
                horizontal = self.horizontal
                depth = self.depth
            case SubmarineCommand(motion=MotionEnm.down, units=units):
                aim = self.aim + units
                horizontal = self.horizontal
                depth = self.depth
            case SubmarineCommand(motion=MotionEnm.forward, units=units):
                aim = self.aim
                horizontal = self.horizontal + units
                depth = self.depth + (self.aim * units)
            case _:
                aim = self.aim
                horizontal = self.horizontal
                depth = self.depth

        return SubmarineState(horizontal=horizontal, depth=depth, aim=aim)

    def apply_many(self, commands: Iterable[SubmarineCommand]) -> Self:
        s = self
        for c in commands:
            s = s.apply_command(c)
        return s


ResultAggregate = namedtuple("ResultAggregate", ["forward", "up", "down"])


def parse_input(instream: Iterable[str]) -> Iterable[SubmarineCommand]:
    def parse(s):
        motion, units = s.split(" ", 2)
        data = {"motion": motion, "units": units}
        return parse_obj_as(SubmarineCommand, data)

    s = map(parse, instream)
    return s


def sum_by_motion(instream: Iterable[SubmarineCommand]) -> ResultAggregate:
    s1, s2, s3 = it.tee(instream, 3)
    forward = filter(lambda s: s.motion == MotionEnm.forward, s1)
    up = filter(lambda s: s.motion == MotionEnm.up, s2)
    down = filter(lambda s: s.motion == MotionEnm.down, s3)
    result = ResultAggregate(
        sum(map(lambda s: s.units, forward)),
        sum(map(lambda s: s.units, up)),
        sum(map(lambda s: s.units, down)),
    )
    return result


def solve_part1(instream: Iterable[SubmarineCommand]) -> int:
    aggregate = sum_by_motion(instream)
    return (aggregate.down - aggregate.up) * aggregate.forward


def solve_part2(instream: Iterable[SubmarineCommand]) -> int:
    sub = SubmarineState().apply_many(instream)
    return sub.horizontal * sub.depth


solver01 = Solver(
    parser=parse_input,  # type: ignore
    solver=solve_part1,  # type: ignore
)

solver02 = Solver(
    parser=parse_input,  # type: ignore
    solver=solve_part2,  # type: ignore
)


def main():
    print("Day 01 - Part01 :", solver01.solve(INPATH))
    print("Day 01 - Part02 :", solver02.solve(INPATH))
