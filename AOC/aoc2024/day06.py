import itertools as I
import sys
from enum import IntEnum
from pprint import pprint
from typing import Annotated, Iterator, Literal, Set, Tuple, TypeVar

import numpy as np
import numpy.typing as npt

Position = Tuple[int, int]


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    @classmethod
    def new(cls, value):
        return cls(value)

    def offset(self) -> Position:
        match self.value:
            case 0:
                return np.array([-1, 0])
            case 1:
                return np.array([0, 1])
            case 2:
                return np.array([1, 0])
            case 3:
                return np.array([0, -1])

    def right(self):
        return self.new((self.value + 1) % 4)

    @classmethod
    def from_str(cls, s: str):
        match s:
            case "<":
                return cls.W
            case ">":
                return cls.E
            case "^":
                return cls.N
            case "v":
                return cls.S
        raise ValueError("unhandled char", s)


Guard = Tuple[Position, Direction]


def find_guard(grid: np.ndarray) -> Guard:
    p = np.nonzero(np.isin(grid, ["<", ">", "^", "v"]))
    p = (p[0].item(), p[1].item())
    v = grid[p][0]
    return p, Direction.from_str(v)


def next_pos(g: Position, o: Position) -> Position:
    return int(g[0] + o[0]), int(g[1] + o[1])


def is_in(p: Position, g: np.ndarray) -> bool:
    return (0 <= p[0] < g.shape[0]) and (0 <= p[1] < g.shape[1])


def compute_path(grid: np.ndarray, g: Guard) -> Set[Position]:
    visited = set()
    visited.add(g[0])

    run = True
    while run:
        p = next_pos(g[0], g[1].offset())
        if is_in(p, grid):
            if grid[p] != "#":
                visited.add(p)
                g = (p, g[1])
            else:
                g = (g[0], g[1].right())
        else:
            run = False
    return visited


def is_loop(grid: np.ndarray, g: Guard) -> bool:
    path = set()

    run = True
    while run:
        path.add(g)
        p = next_pos(g[0], g[1].offset())
        if (p, g[1]) in path:
            return True
        elif is_in(p, grid):
            if grid[p] != "#":
                g = (p, g[1])
            else:
                g = (g[0], g[1].right())
        else:
            return False


def part01(pipe: Iterator[str]):
    data = []
    for l in pipe:
        data.append(list(l.strip()))

    grid = np.array(data)
    g = find_guard(grid)

    visited = compute_path(grid, g)
    return len(visited)


def part02(pipe: Iterator[str]):
    data = []
    for l in pipe:
        data.append(list(l.strip()))

    grid = np.array(data)
    g = find_guard(grid)

    visited = compute_path(grid, g)
    visited.remove(g[0])

    count = 0
    for p in visited:
        newgrid = np.copy(grid)
        newgrid[p] = "#"
        count += is_loop(newgrid, g)
    return count
