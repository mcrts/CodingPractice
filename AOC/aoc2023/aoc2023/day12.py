import sys
import re

import itertools as I
import functools as F
from pprint import pprint

from typing import NamedTuple, Tuple
from collections import Counter

RE_T = r"[#\.\?]"
RE_Tp = r"[#\?]"
RE_Td = r"[\.\?]"

class Report(NamedTuple):
    bits: str
    groups: Tuple[int, ...]

    @classmethod
    def from_string(cls, s):
        bits, groups = s.split(' ', 1)
        groups = tuple(map(int, groups.split(',')))
        return cls(bits, groups)
    
    @classmethod
    def from_folded(cls, s):
        bits, groups = s.split(' ', 1)
        groups = tuple(map(int, groups.split(',')))

        bits_f = "?".join([bits] * 5)
        groups_f = groups * 5
        return cls(bits_f, groups_f)
    
class BruteForceSolver:
    @staticmethod
    def regexp(report):
        reg_start = rf"^{RE_Td}*"
        reg_end = rf"{RE_Td}*$"
        reg = rf"{RE_Td}+".join(["%s{%s}" % (RE_Tp, n) for n in report.groups])
        return reg_start + reg + reg_end

    @classmethod
    def match(cls, report):
        regexp = cls.regexp(report)
        m = re.match(regexp, report.bits)
        return m

    def handle_basecase(self, report: Report) -> Tuple[bool, int]:
        N = len(report.groups)
        C = Counter(report.bits)
        m = bool(self.match(report))

        match m, N, C["#"]:
            case False, _, _:
                return True, 0 
            case True, 0, 0:
                return True, 1
            case _:
                return False, -1

    def solve(self, report: Report) -> int:
        cond, v = self.handle_basecase(report)
        if cond:
            return v

        h = report.bits[0]
        N = len(report.groups)
        match h, N:
            case ".", _ :
                r = Report(report.bits[1:], report.groups)
                return self.solve(r)
            case "?", _ :
                r0 = Report(report.bits[1:], report.groups)
                r1 = Report("#" + report.bits[1:], report.groups)
                return self.solve(r0) + self.solve(r1)
            case "#", 1 :
                k = report.groups[0]
                b0 = report.bits[:k]
                r0 = Report(b0, (k,))
                g1 = report.groups[1:]
                b1 = report.bits[k:]
                r1 = Report(b1, g1)
                return self.solve(r1)
            case '#', n :
                k = report.groups[0]
                b0 = report.bits[:k]
                r0 = Report(b0, (k,))
                g1 = report.groups[1:]
                b1 = report.bits[k+1:]
                r1 = Report(b1, g1)
                return self.solve(r1)
            case _ :
                return -1


class DPSolver:
    @staticmethod
    def regexp(report):
        g = report.groups[0]
        l1 = len(report.groups[1:]) + sum(report.groups[1:]) - 1
        reg = rf"^{RE_T}*" + "%s{%s}" % (RE_Tp, g) + "%s%s{%s,}" % (RE_Td, RE_T, l1)
        return reg

    @classmethod
    def match(cls, report):
        regexp = cls.regexp(report)
        m = re.match(regexp, report.bits)
        return m

    def subproblem_iterator(self, report):
        reg = self.regexp(report)
        for i in range(len(report.bits)):
            bits = report.bits[i:]
            if re.match(reg, bits):
                yield i

    def solve(self, report: Report) -> int:
        for i in self.subproblem_iterator(report):
            print(i, report.bits[i:])
        return 0


def part1(pipe):
    solver = DPSolver()
    count = 0
    for l in pipe:
        r = Report.from_string(l.strip())
        print("SOLVING", r)
        c = solver.solve(r)
        print("COUNT", c)
        count += c
        print()
    return count

def part2(pipe):
    solver = BruteForceSolver()
    count = 0
    for l in pipe:
        r = Report.from_folded(l.strip())
        print("SOLVING", r)
        c = solver.solve(r)
        print("COUNT", c)
        count += c
        print()
    return 0
