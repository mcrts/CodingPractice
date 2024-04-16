import sys
import re

import itertools as I
import functools as F
from collections import namedtuple
from pprint import pprint


def transpose(rows):
    lx = len(rows)
    ly = len(rows[0])
    panel = tuple(["".join([rows[x][y] for x in range(lx)]) for y in range(ly)])
    return panel


def tilt(panel):
    panel = transpose(panel)
    new_panel = []
    for r in panel:
        nr = "#".join([''.join(sorted(s, reverse=True)) for s in r.split('#')])
        new_panel.append(nr)
    new_panel = transpose(new_panel)
    return new_panel


def cycle(panel):
    # Orient North, Sort REV for tilting North
    panel = transpose(panel)
    panel = [
        "#".join([''.join(sorted(s, reverse=True)) for s in r.split('#')])
        for r in panel
    ]

    # Orient West, Sort REV for tilting West
    panel = transpose(panel)
    panel = [
        "#".join([''.join(sorted(s, reverse=True)) for s in r.split('#')])
        for r in panel
    ]
    
    # Orient North, Sort for tilting South
    panel = transpose(panel)
    panel = [
        "#".join([''.join(sorted(s)) for s in r.split('#')])
        for r in panel
    ]

    # Orient West, Sort for tilting East
    panel = transpose(panel)
    panel = [
        "#".join([''.join(sorted(s)) for s in r.split('#')])
        for r in panel
    ]
    return panel


def hash_panel(panel):
    s = "".join(panel)
    return hash(s)


def part1(pipe):
    panel = []
    for l in pipe:
        panel.append(l.strip())
    
    panel = tilt(panel)

    res = 0
    for i, row in enumerate(panel[::-1]):
        res += ((i+1) * row.count("O"))
    return res

def part2(pipe):
    panel = []
    for l in pipe:
        panel.append(l.strip())

    track = []
    states = set()
    h = hash_panel(panel)
    track.append(h)
    states.add(h)

    i = 1_000_000_000
    while i > 0:
        i -= 1
        panel = cycle(panel)
        h = hash_panel(panel)
        if h in states:
            k = len(track) - track.index(h)
            r = i % k
            i = r
        track.append(h)
        states.add(h)

    res = sum([((idx+1) * r.count("O")) for idx, r in enumerate(panel[::-1])])
    return res
