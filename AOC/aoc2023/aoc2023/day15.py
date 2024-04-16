import sys
import re

import itertools as I
import functools as F
from collections import namedtuple, OrderedDict
from pprint import pprint

def hash_line(line):
    v = 0
    for c in line:
        v += ord(c)
        v = (v * 17) % 256
    return v

def part1(pipe):
    lines = next(pipe).strip().split(',')
    res = 0
    for l in lines:
        h = hash_line(l)
        res += h
    return res

def part2(pipe):
    lines = next(pipe).strip().split(',')
    reg = re.compile(r'(\w+)([=-])(\d*)')
    array = [OrderedDict() for _ in range(256)]
    for l in lines:
        label, action, strength = re.match(reg, l).groups()
        box = array[hash_line(label)]
        match action:
            case '-':
                box.pop(label, default=None)
            case '=':
                box[label] = int(strength)
    power = 0
    for i, b in enumerate(array):
        if b:
            bpower = (1 + i)
            for j, f in enumerate(b.values()):
                power += bpower * (j + 1) * (f)
    return power
