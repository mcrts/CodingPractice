from collections import namedtuple
import sys
import re
import functools as F

DELTAS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]
SYMBOL_GROUP = r"[\#\&\*\-\@\%\$\/\+\=]"
RE_SYMBOL = rf"(?P<symbol>{SYMBOL_GROUP})"
RE_PART = r"(?P<part>\d+)"
RE_PATTERN1 = '|'.join([RE_PART, RE_SYMBOL])

RE_GEAR = r"(?P<gear>\*)"
RE_PATTERN2 = '|'.join([RE_PART, RE_GEAR])

Part = namedtuple('Part', ['index', 'value'])

def is_symbol(c):
    return not (c.isdigit() or c == ".")

def neighbours(index):
    i, j = index
    return {(i + di, j + dj) for di, dj in DELTAS}

def part1():
    symbols = set()
    parts = dict()
    for i, l in enumerate(sys.stdin):
        l = l.strip()
        for m in re.finditer(RE_PATTERN1, l):
            match m.lastgroup:
                case 'part':
                    index = (i, m.start())
                    for x in range(m.start(), m.end()):
                        parts[(i, x)] = Part(index, int(m.group()))
                case 'symbol':
                    index = (i, m.start())
                    symbols = symbols.union(neighbours(index))

    selected_parts = set(map(parts.get, symbols.intersection(parts.keys())))
    return sum(map(lambda p: p.value, selected_parts))

def part2():
    gears = set()
    parts = dict()
    for i, l in enumerate(sys.stdin):
        l = l.strip()
        for m in re.finditer(RE_PATTERN2, l):
            match m.lastgroup:
                case 'part':
                    index = (i, m.start())
                    for x in range(m.start(), m.end()):
                        parts[(i, x)] = Part(index, int(m.group()))
                case 'gear':
                    index = (i, m.start())
                    gears.add(index)

    selected_gears = list(filter(
        lambda s: len(s) == 2,
        [
            list(set(map(
                parts.get,
                neighbours(g).intersection(parts.keys())
            )))
        for g in gears
        ]
    ))
    return sum(map(lambda g: g[0].value * g[1].value, selected_gears))

def main():
    v = part2()
    print(v)