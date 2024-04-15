import sys
import re

import itertools as I
import functools as F
from collections import namedtuple
from pprint import pprint

Puzzle = namedtuple("Puzzle", ['v', 'h'])
def puzzle_from_rows(rows):
    h = tuple(rows)
    lx = len(h)
    ly = len(h[0])
    v = tuple(["".join([h[x][y] for x in range(lx)]) for y in range(ly)])
    return Puzzle(v, h)

def mirror(p, l, r):
    if l < 0 or (r >= len(p)):
        return True

    if p[l] == p[r]:
        return mirror(p, l-1, r+1)
    else:
        return False

def mirror_at(p, idx):
    return mirror(p, idx-1, idx)

def part1(pipe):
    rows = []
    puzzles = []
    v_result = 0
    h_result = 0
    for l in pipe:
        if l == "\n":
            puzzles.append(puzzle_from_rows(rows))
            rows = []
        else:
            rows.append(l.strip())
    puzzles.append(puzzle_from_rows(rows))

    for p in puzzles:
        for i in range(1, len(p.v)):
            if mirror_at(p.v, i):
                v_result += i
        
        for i in range(1, len(p.h)):
            if mirror_at(p.h, i):
                h_result += i

    return v_result + 100 * h_result



def mirror_count(p, l, r):
    if l < 0 or (r >= len(p)):
        return 0
    
    count = sum(map(lambda x: x[0] != x[1], zip(p[l], p[r])))
    if count <= 1:
        return count + mirror_count(p, l-1, r+1)
    else:
        return float("inf")

def mirror_at_count(p, idx):
    return mirror_count(p, idx-1, idx)


def part2(pipe):
    rows = []
    puzzles = []
    v_result = 0
    h_result = 0
    for l in pipe:
        if l == "\n":
            puzzles.append(puzzle_from_rows(rows))
            rows = []
        else:
            rows.append(l.strip())
    puzzles.append(puzzle_from_rows(rows))

    for p in puzzles:
        for i in range(1, len(p.v)):
            if mirror_at_count(p.v, i) == 1:
                v_result += i
        
        for i in range(1, len(p.h)):
            if mirror_at_count(p.h, i) == 1:
                h_result += i

    return v_result + 100 * h_result
