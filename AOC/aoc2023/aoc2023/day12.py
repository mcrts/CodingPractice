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
    
    @classmethod
    def reduce(cls, r):
        bits = '.'.join(filter(bool, r.bits.split('.')))
        return cls(bits, r.groups)

class Matcher:
    @staticmethod
    def regexp_single(l, k, i):
        reg = '^%s{%d}' % (RE_Td, i)
        reg += '%s{%d}' % (RE_Tp, k)
        reg += '%s{%d}$' % (RE_Td, l-k-i)
        return reg
    
    @staticmethod
    def regexp_double(l, k, i):
        reg = '^%s{%d}' % (RE_T, i)
        reg += '%s{%d}' % (RE_Td, 1)
        reg += '%s{%d}' % (RE_Tp, k)
        reg += '%s{%d}$' % (RE_Td, l - k - i - 1)
        return reg
    
    @staticmethod
    def regexp_multi(l, k, i):
        reg = '^%s{%d}' % (RE_T, i)
        reg += '%s{%d}' % (RE_Td, 1)
        reg += '%s{%d}' % (RE_Tp, k)
        reg += '%s{%d}' % (RE_Td, 1)
        reg += '%s{%d}$' % (RE_T, l - k - i - 2)
        return reg


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
            
class SingleSolver:
    @classmethod
    @F.lru_cache(maxsize=512)
    def _solve(cls, report: Report) -> int:
        l = len(report.bits)
        k = report.groups[0]
        c = 0
        for i in range(l):
            reg = Matcher.regexp_single(l, k, i)
            c += bool(re.match(reg, report.bits))

        return c

    def solve(self, report: Report) -> int:
        if len(report.groups) != 1:
            raise ValueError(f"Can only solve size 1 problem, was given a size {len(report.groups)} problem", report)
        
        if report.bits[0] == "." or report.bits[-1] == ".":
            report = Report.reduce(report)
        
        return self._solve(report)
    
SINGLE_SOLVER = SingleSolver()
class DoubleSolver:
    single_solver = SINGLE_SOLVER

    @classmethod
    @F.lru_cache(maxsize=512)
    def _solve(cls, report: Report) -> int:
        l = len(report.bits)
        k1, k2 = report.groups
        c = 0
        for i in range(k1, l-k2):
            reg = Matcher.regexp_double(l, k2, i)
            if bool(re.match(reg, report.bits)):
                r1 = Report(report.bits[:i], (k1,))
                c += cls.single_solver.solve(r1)
        return c

    def solve(self, report: Report) -> int:
        if len(report.groups) != 2:
            raise ValueError(f"Can only solve size 2 problem, was given a size {len(report.groups)} problem", report)

        if report.bits[0] == "." or report.bits[-1] == ".":
            report = Report.reduce(report)
        
        return self._solve(report)

DOUBLE_SOLVER = DoubleSolver()

class DPSolver:
    single_solver = SINGLE_SOLVER
    double_solver = DOUBLE_SOLVER

    @F.lru_cache(maxsize=512)
    def _solve(self, report: Report) -> int:

        match len(report.groups):
            case 0:
                raise ValueError("0 groups", report)
            case 1:
                return self.single_solver.solve(report)
            case 2:
                return self.double_solver.solve(report)
            case _:
                midx = len(report.groups) // 2
                g1 = report.groups[:midx]
                g2 = report.groups[midx+1:]
                m = report.groups[midx]
                
                l = len(report.bits)
                k1 = sum(g1) + len(g1) - 1
                k2 = sum(g2) + len(g2) + m
                c = 0
                for i in range(k1, l-k2):
                    reg = Matcher.regexp_multi(l, m, i)
                    if bool(re.match(reg, report.bits)):
                        r1 = Report(report.bits[:i], g1)
                        r2 = Report(report.bits[i+m+2:], g2)
                        c += self.solve(r1) * self.solve(r2)
                return c

    def solve(self, report: Report) -> int:
        if report.bits[0] == "." or report.bits[-1] == ".":
            report = Report.reduce(report)
        
        return self._solve(report)


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
    solver = DPSolver()
    count = 0
    for i, l in enumerate(pipe):
        r = Report.from_folded(l.strip())
        print(f"SOLVING {i}-th problem", r)
        c = solver.solve(r)
        print("COUNT", c)
        count += c
        print()
    return count
