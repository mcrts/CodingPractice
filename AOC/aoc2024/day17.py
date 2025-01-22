import itertools as I
import re
import sys
from dataclasses import dataclass, field
from pprint import pprint
from typing import Callable, ClassVar, Iterable, Iterator, List, Mapping, Tuple

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
        opcodes = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]
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


def part02(pipe: Iterator[str]):
    """SOLVE with DP, need a static computer state"""
    computer, program = parse_input(pipe)
    a = 0
    while True:
        c = Computer(ra=a, rb=computer.rb, rc=computer.rc)
        output = c.run(program)
        if output == program:
            return a
        a += 1
    return -1
