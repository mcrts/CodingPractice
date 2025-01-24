import itertools as I
import sys
from pprint import pprint
from typing import Iterator, List, NamedTuple, Tuple

import numpy as np

Position = Tuple[int, int]


class Path(NamedTuple):
    head: Position
    trail: Tuple[Position, ...]


def get_children(grid: np.ndarray, p: Position) -> List[Position]:
    i, j = p
    children = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    children = [
        c
        for c in children
        if 0 <= c[0] < grid.shape[0] and 0 <= c[1] < grid.shape[1] and grid[c]
    ]
    return children


def bfs(grid: np.ndarray, start: Position, end: Position) -> Path:
    path = Path(start, (start,))

    visited = set()
    queue = [path]
    while queue:
        p = queue.pop(0)
        if p.head == end:
            return p

        visited.add(p.head)
        for c in get_children(grid, p.head):
            if c not in visited:
                queue.append(Path(c, p.trail + (c,)))

    return None


def part01(pipe: Iterator[str]):
    grid = np.full((71, 71), fill_value=True)
    for _, l in zip(range(1024), pipe):
        i, j = tuple(map(int, l.strip().split(",")))
        grid[j, i] = False

    path = bfs(grid, (0, 0), (70, 70))
    return len(path.trail) - 1


def part02(pipe: Iterator[str]):
    return 0
