from collections import namedtuple
import sys
import re
import itertools as I
import functools as F
import math as M
import decimal as D

RE_TIME = r"^Time:\s+(?P<times>.*)$"
RE_DISTANCE = r"^Distance:\s+(?P<distances>.*)$"
RE_DIGIT = r"(\d+)"


def solve_quad(a, b, c):
    d = (b**2) - (4*a*c)
    if d < 0:
        return None, None
    elif d == 0:
        return (-b / (2*a), -b / (2*a))
    elif d > 0:
        x0 = (-b - M.sqrt(d)) / (2*a)
        x1 = (-b + M.sqrt(d)) / (2*a)
        return x1, x0


Race = namedtuple("Race", ['time', 'distance'])
class Race(Race):
    def solve(self):
        e = 0.00000000001
        x0, x1 = solve_quad(-1, self.time, -self.distance)
        if x0:
            x0 = M.ceil(x0 + e)
        if x1:
            x1 = M.floor(x1 - e)
        return x1 - x0 + 1

def part1():
    ltime = sys.stdin.readline()
    m = re.match(RE_TIME, ltime.strip())
    times = map(int, re.findall(RE_DIGIT, m.group('times')))

    ldistance = sys.stdin.readline()
    m = re.match(RE_DISTANCE, ldistance.strip())
    distances = map(int, re.findall(RE_DIGIT, m.group('distances')))
    
    scores = [Race(t, d).solve() for t, d in zip(times, distances)]
    score = F.reduce(int.__mul__, scores)
    return score

def part2():
    ltime = sys.stdin.readline()
    m = re.match(RE_TIME, ltime.strip())
    t = int(m.group('times').strip().replace(" ", ""))

    ldistance = sys.stdin.readline()
    m = re.match(RE_DISTANCE, ldistance.strip())
    d = int(m.group('distances').strip().replace(" ", ""))
    
    r = Race(t, d)
    return r.solve()

def main():
    v = part2()
    print(v)