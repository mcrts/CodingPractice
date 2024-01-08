import sys
import re

import itertools as I
import functools as F
from collections import namedtuple
from pprint import pprint



def rec_solve1(arr):
    diffs = [b-a for a, b in zip(arr[:-1], arr[1:])]
    if len(set(diffs)) == 1:
        d = diffs[0]
    else:
        d = rec_solve1(diffs)
    return arr[-1] + d

def rec_solve2(arr):
    diffs = [b-a for a, b in zip(arr[:-1], arr[1:])]
    if len(set(diffs)) == 1:
        d = diffs[0]
    else:
        d = rec_solve2(diffs)
    return arr[0] - d

def part1(pipe):
    v = 0
    for l in pipe:
        numbers = list(map(int, l.strip().split(" ")))
        v += rec_solve1(numbers)
    return v

def part2(pipe):
    v = 0
    for l in pipe:
        numbers = list(map(int, l.strip().split(" ")))
        d = rec_solve2(numbers)
        v += d
    return v

def main():
    pipe1, pipe2 = I.tee(sys.stdin, 2)
    print(f"Part 1: {part1(pipe1)}")
    print(f"Part 2: {part2(pipe2)}")
