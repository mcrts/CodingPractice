import functools as F
import itertools as I
import re
import sys
from dataclasses import dataclass, field
from itertools import tee
from pprint import pprint
from types import GeneratorType
from typing import (
    Callable,
    ClassVar,
    Iterable,
    Iterator,
    List,
    Mapping,
    NamedTuple,
    Self,
    Tuple,
)

RE_REG = r"Register ([ABC]): (\d+)"
RE_PROG = r"Program: (([0-8],{0,1})+)"


@dataclass
class Computer:
    ra: int
    rb: int
    rc: int
    pointer: int = 0
    output: Tuple[int, ...] = field(default_factory=tuple)

    def combo(self, operand: int) -> int:
        match operand:
            case 4:
                return self.ra
            case 5:
                return self.rb
            case 6:
                return self.rc
            case 7:
                raise ValueError("Unexpected operand 7")
            case x:
                return x

    def adv(self, operand: int):
        """opcode 0"""
        self.ra = self.ra // 2 ** self.combo(operand)
        self.pointer += 2

    def bxl(self, operand: int):
        """opcode 1"""
        self.rb = self.rb ^ operand
        self.pointer += 2

    def bst(self, operand: int):
        """opcode 2"""
        self.rb = self.combo(operand) % 8
        self.pointer += 2

    def jnz(self, operand: int):
        """opcode 3"""
        if self.ra == 0:
            self.pointer += 2
        else:
            self.pointer = operand

    def bxc(self, operand: int):
        """opcode 4"""
        self.rb = self.rb ^ self.rc
        self.pointer += 2

    def out(self, operand: int):
        """opcode 5"""
        self.output = self.output + (self.combo(operand) % 8,)
        self.pointer += 2

    def bdv(self, operand: int):
        """opcode 6"""
        self.rb = self.ra // 2 ** self.combo(operand)
        self.pointer += 2

    def cdv(self, operand: int):
        """opcode 7"""
        self.rc = self.ra // 2 ** self.combo(operand)
        self.pointer += 2

    def run(self, program: Tuple[int, ...]) -> Tuple[int, ...]:
        opcodes = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
        while self.pointer < len(program) - 1:
            instr, operand = program[self.pointer : self.pointer + 2]
            opcodes[instr](operand)
        return self.output


def parse_input(pipe: Iterator[str]) -> Tuple[Computer, Tuple[int, ...]]:
    registers = dict()
    for _, l in zip(range(3), pipe):
        m = re.match(RE_REG, l)
        k, v = m.groups()
        registers[k] = int(v)

    next(pipe)
    m = re.match(RE_PROG, next(pipe))
    program = tuple(map(int, m.group(1).split(",")))

    return Computer(ra=registers["A"], rb=registers["B"], rc=registers["C"]), program


def part01(pipe: Iterator[str]):
    computer, program = parse_input(pipe)
    output = computer.run(program)
    return ",".join(map(str, output))


Output = Tuple[int, ...]


class ComputerState(NamedTuple):
    program: Tuple[int, ...]
    ra: int
    rb: int
    rc: int
    pointer: int

    @classmethod
    def make(cls, program: Tuple[int, ...], ra: int, rb: int, rc: int, pointer: int) -> Self:
        return cls(program, ra, rb, rc, pointer)

    def combo(self, operand: int) -> int:
        match operand:
            case 4:
                return self.ra
            case 5:
                return self.rb
            case 6:
                return self.rc
            case 7:
                raise ValueError("Unexpected operand 7")
            case x:
                return x

    def adv(self, operand: int) -> Tuple[Self, Output]:
        """opcode 0"""
        ra = self.ra // 2 ** self.combo(operand)
        pointer = self.pointer + 2
        return (
            self.make(program=self.program, ra=ra, rb=self.rb, rc=self.rc, pointer=pointer),
            tuple(),
        )

    def bxl(self, operand: int) -> Tuple[Self, Output]:
        """opcode 1"""
        rb = self.rb ^ operand
        pointer = self.pointer + 2
        return (
            self.make(program=self.program, ra=self.ra, rb=rb, rc=self.rc, pointer=pointer),
            tuple(),
        )

    def bst(self, operand: int) -> Tuple[Self, Output]:
        """opcode 2"""
        rb = self.combo(operand) % 8
        pointer = self.pointer + 2
        return (
            self.make(program=self.program, ra=self.ra, rb=rb, rc=self.rc, pointer=pointer),
            tuple(),
        )

    def jnz(self, operand: int) -> Tuple[Self, Output]:
        """opcode 3"""
        if self.ra == 0:
            pointer = self.pointer + 2
        else:
            pointer = operand
        return (
            self.make(program=self.program, ra=self.ra, rb=self.rb, rc=self.rc, pointer=pointer),
            tuple(),
        )

    def bxc(self, operand: int) -> Tuple[Self, Output]:
        """opcode 4"""
        rb = self.rb ^ self.rc
        pointer = self.pointer + 2
        return (
            self.make(program=self.program, ra=self.ra, rb=rb, rc=self.rc, pointer=pointer),
            tuple(),
        )

    def out(self, operand: int) -> Tuple[Self, Output]:
        """opcode 5"""
        output = (self.combo(operand) % 8,)
        pointer = self.pointer + 2
        return (
            self.make(program=self.program, ra=self.ra, rb=self.rb, rc=self.rc, pointer=pointer),
            output,
        )

    def bdv(self, operand: int) -> Tuple[Self, Output]:
        """opcode 6"""
        rb = self.ra // 2 ** self.combo(operand)
        pointer = self.pointer + 2
        return (
            self.make(program=self.program, ra=self.ra, rb=rb, rc=self.rc, pointer=pointer),
            tuple(),
        )

    def cdv(self, operand: int) -> Tuple[Self, Output]:
        """opcode 7"""
        rc = self.ra // 2 ** self.combo(operand)
        pointer = self.pointer + 2
        return (
            self.make(program=self.program, ra=self.ra, rb=self.rb, rc=rc, pointer=pointer),
            tuple(),
        )

    def run_once(self) -> Tuple[bool, Self, Output]:
        opcodes = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
        if self.pointer < len(self.program) - 1:
            instr, operand = self.program[self.pointer : self.pointer + 2]
            cs, output = opcodes[instr](operand)
            return False, cs, output
        else:
            return True, self, tuple()


@F.lru_cache()
def run_once(cs: ComputerState) -> Tuple[bool, ComputerState, Output]:
    stop = False
    out = tuple()
    while not stop:
        stop, cs, out = cs.run_once()
        if out:
            return stop, cs, out
    return stop, cs, out


def streaming_run(cs: ComputerState) -> Iterator[int]:
    stop = False
    while not stop:
        stop, cs, out = run_once(cs)
        if out:
            yield out[0]


def stream_compare(s0: Iterator[int], s1: Iterator[int]) -> bool:
    for x, y in I.zip_longest(s0, s1, fillvalue=None):
        if x != y:
            return False

    return True


def part02(pipe: Iterator[str]):
    """SOLVE with DP, need a static computer state"""
    computer, program = parse_input(pipe)
    rb = int(computer.rb)
    rc = int(computer.rc)

    for a in I.count(0, 1):
        if a % 1000000 == 0:
            print(a)
        cs = ComputerState(program, a, rb, rc, 0)
        if stream_compare(program, streaming_run(cs)):
            print(program, tuple(streaming_run(cs)))
            return a

    """
    for a in I.count(0, 1):
        cs = ComputerState(program, a, rb, rc, 0)
        if run(cs) == program:
            return a
    """
    return -1
