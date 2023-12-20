import sys
import re
import numpy as np
import numpy.typing as npt

import itertools as I
import functools as F
from collections import namedtuple
from pprint import pprint
from dataclasses import dataclass

CONNECT_TO = {
    b'S': set(['north', 'east', 'south', 'west']),
    b'|': set(['north', 'south']),
    b'-': set(['east', 'west']),
    b'J': set(['north', 'west']),
    b'7': set(['south', 'west']),
    b'F': set(['east', 'south']),
    b'L': set(['north', 'east']),
    b'.': set(),
    None: set(),
}
CONNECT_FROM = {
    b'S': set(['north', 'east', 'south', 'west']),
    b'|': set(['north', 'south']),
    b'-': set(['east', 'west']),
    b'J': set(['east', 'south']),
    b'7': set(['north', 'east']),
    b'F': set(['north', 'west']),
    b'L': set(['south', 'west']),
    b'.': set(),
    None: set(),
}
Node = namedtuple("Node", ('idx', 'value'))
class Node(Node):
    @classmethod
    def NULL(cls):
        return cls(None, None)
    
    def __bool__(self):
        return bool(self.idx) and bool(self.value)
    
    def connect(lhs, rhs, connection):
        match (bool(lhs), bool(rhs), connection in CONNECT_TO[lhs.value], connection in CONNECT_FROM[rhs.value]):
            case True, True, True, True:
                return True
            case _:
                return False

Path = namedtuple("Path", ('nodes'))
class Path(Path):
    def explored(self):
        return set(self.nodes)
    
    def __len__(self):
        return len(self.nodes)

    @classmethod
    def add(cls, path, node):
        return cls(path.nodes + (node,))


@dataclass
class Graph:
    _grid: npt.ArrayLike

    def __init__(self, grid):
        self._grid = grid 
    
    def get(self, idx):
        i, j  = idx
        match (0 <= i < self._grid.shape[0] and 0 <= j < self._grid.shape[1]):
            case False:
                return Node.NULL()
            case True:
                v = self._grid[idx]
                return Node(idx, v)

    def start(self):
        for idx, v in np.ndenumerate(self._grid):
            if v == b'S':
                return Node(idx, v)
        return Node.NULL()
    
    def adjacent_nodes(self, node):
        idx = node.idx
        north = self.get((idx[0] - 1, idx[1]))
        east = self.get((idx[0], idx[1] + 1))
        south = self.get((idx[0] + 1, idx[1]))
        west = self.get((idx[0], idx[1] - 1))

        north = north if node.connect(north, 'north') else Node.NULL()
        east = east if node.connect(east, 'east') else Node.NULL()
        south = south if node.connect(south, 'south') else Node.NULL()
        west = west if node.connect(west, 'west') else Node.NULL()
        return tuple(filter(bool, [north, east, south, west]))

    def iterate(self, path):
        while True:
            n = path.nodes[-1]
            children = set(self.adjacent_nodes(n))
            child = children.difference(path.explored())
            if child:
                path = Path.add(path, child.pop())
                yield path
            else:
                break

def part1(pipe):
    grid = []
    for l in pipe:
        grid.append(list(l.strip()))
    g = Graph(np.array(grid, dtype='|S1'))
    s = g.start()

    path = Path(tuple([s]))
    c, _ = g.adjacent_nodes(s)
    path = Path.add(path, c)
    for p in g.iterate(path):
        pass
    return g, p


def part2(graph, path):
    c = 0
    g = np.full_like(graph._grid, ".")
    for node in path.nodes:
        g[node.idx] = node.value
    
    nrow, ncol = g.shape
    path_indices = set([n.idx for n in path.nodes])

    for i in range(nrow):
        inside_flag = False
        up_flag = False
        down_flag = False
        for j in range(ncol):
            idx = (i, j)
            v = g[idx]
            is_border = (idx in path_indices)
            match (is_border, v):
                case (True, b'|'):
                    up_flag = True
                    down_flag = True
                case (True, b'-'):
                    pass
                case (True, b'F'):
                    down_flag = not down_flag
                case (True, b'J'):
                    up_flag = not up_flag
                case (True, b'L'):
                    up_flag = not up_flag
                case (True, b'7'):
                    down_flag = not down_flag
                case _:
                    pass
            
            if up_flag and down_flag:
                inside_flag =  not inside_flag
                up_flag = False
                down_flag = False

            is_empty = (v == b'.')

            if is_empty and inside_flag:
                g[idx] = 1
                c += 1
    return c

def main():
    graph, path = part1(sys.stdin)
    print(f"Part 1: {len(path) // 2}")
    print(f"Part 2: {part2(graph, path)}")
