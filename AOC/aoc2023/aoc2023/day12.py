import sys
import re

import itertools as I
import functools as F
from pprint import pprint

from typing import NamedTuple, Tuple
from collections import Counter

class Report(NamedTuple):
    bits: str
    groups: Tuple[int, ...]

    @classmethod
    def from_string(cls, s):
        bits, groups = s.split(' ', 1)
        groups = tuple(map(int, groups.split(',')))
        return cls(bits, groups)
    
    def verify(self):
        c = Counter(self.bits)
        k = sum(self.groups)
        n = len(self.groups)


        if k + n - 1 > len(self.bits):
            return False
        if c["#"] > k:
            return False
        elif k > c["#"] + c["?"]:
            return False
        else:
            return True
 

class BruteForceSolver:
    def process(self, report: Report) -> int:
        #print("PROCESS | ", report)

        h = report.bits[0]
        k = report.groups[0]
        match report.verify(), h:
            case False, _:
                #print("CASE INVALID | ", "->", 0)
                return 0
            case True, ".":
                r = Report(report.bits[1:], report.groups)
                #print("CASE . | ", "->", r)
                return self.solve(r)
            case True, "#":
                b0 = report.bits[:k]
                r0 = Report(b0, (k,))
                if not r0.verify():
                    #print("CASE # | ", r0, "->", 0)
                    return 0
                
                g1 = report.groups[1:]
                if len(g1) == 0:
                    b1 = report.bits[k:]
                    r1 = Report(b1, g1)
                else:
                    if report.bits[k] == "#":
                        #print("CASE # | ", (r0, report.bits[k:]), "->", 0)
                        return 0

                    b1 = report.bits[k+1:]
                    r1 = Report(b1, g1)

                #print("CASE # | ", "->", r1)
                return self.solve(r1)
            case True, "?":
                r0 = Report(report.bits[1:], report.groups)
                r1 = Report("#" + report.bits[1:], report.groups)
                #print("CASE ? | ", "->", r0, r1)
                return self.solve(r0) + self.solve(r1)

        
    def solve(self, report: Report) -> int:
        #print("SOLVE | ", report)

        N = len(report.groups)
        L = len(report.bits)
        C = Counter(report.bits)


        match N, L, C['#']:
            case 0, 0, _:
                #print("CASE 0 0 _ | ", report, "->", 1)
                return 1
            case 0, l, 0:
                #print("CASE 0 l 0 | ", report, "->", 1)
                return 1
            case 0, l, p,:
                #print("CASE 0 l p | ", report, "->", 0)
                return 0
            case n, 0, _:
                #print("CASE n 0 _ | ", report, "->", 0)
                return 0
            case n, l, _:
                #print("CASE n l _ | ", report)
                return self.process(report)
            case _:
                #print(N, L, C)
                return -999

            


def part1(pipe):
    solver = BruteForceSolver()
    count = 0
    for l in pipe:
        r = Report.from_string(l.strip())
        c = solver.solve(r)
        print(r, c)
        count += c
    return count

def part2(pipe):
    for l in pipe:
        print(l.strip())
    return 0
