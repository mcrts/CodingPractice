import sys
import re

import itertools as I
import functools as F
from collections import namedtuple
from pprint import pprint

import numpy as np

RE_POINT = r"#"

def array(pipe):
    grid = []
    for l in pipe:
        l = l.strip()
        row = list(map(lambda c: c == "#", l))
        grid.append(row)
    return np.array(grid)

def expand_axis(grid):
    is_empty = lambda r: r.sum() == 0
    yaxis = np.cumsum(1 + np.apply_along_axis(is_empty, 1, grid))
    xaxis = np.cumsum(1 + np.apply_along_axis(is_empty, 0, grid))
    return xaxis, yaxis
    
def expand_axis2(grid):
    f = 1000000 - 1
    is_empty = lambda r: (r.sum() == 0) * f
    yaxis = np.cumsum(1 + np.apply_along_axis(is_empty, 1, grid))
    xaxis = np.cumsum(1 + np.apply_along_axis(is_empty, 0, grid))
    return xaxis, yaxis
    

def part1(pipe):
    grid = array(pipe)
    xaxis, yaxis = expand_axis(grid)
    points = []
    for index, x in np.ndenumerate(grid):
        if x:
            j, i = index
            points.append(np.array((xaxis[i], yaxis[j])))
    
    pairs = I.combinations(points, 2)
    lengths = map(lambda x: np.abs(x[0] - x[1]).sum(), pairs)
    return sum(lengths)

def part2(pipe):
    grid = array(pipe)
    xaxis, yaxis = expand_axis2(grid)
    points = []
    for index, x in np.ndenumerate(grid):
        if x:
            j, i = index
            points.append(np.array((xaxis[i], yaxis[j])))
    
    pairs = I.combinations(points, 2)
    lengths = map(lambda x: np.abs(x[0] - x[1]).sum(), pairs)
    return sum(lengths)