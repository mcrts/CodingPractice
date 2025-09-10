import heapq as H
import itertools as I
import sys
from dataclasses import dataclass, field
from enum import IntEnum
from pprint import pprint
from typing import Iterable, Iterator, NamedTuple, Tuple

import networkx as nx
import numpy as np


class Position(NamedTuple):
    x: int
    y: int


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    @classmethod
    def new(cls, value):
        return cls(value)

    def right(self):
        return self.new((self.value + 1) % 4)

    def left(self):
        return self.new((self.value - 1) % 4)

    def offset(self):
        match self.value:
            case 0:
                return (-1, 0)
            case 1:
                return (0, 1)
            case 2:
                return (1, 0)
            case 3:
                return (0, -1)


class Node(NamedTuple):
    pos: Position
    direction: Direction

    def forward(self):
        dx, dy = self.direction.offset()
        p = Position(self.pos.x + dx, self.pos.y + dy)
        return Node(p, self.direction)

    def left(self):
        return Node(self.pos, self.direction.left())

    def right(self):
        return Node(self.pos, self.direction.right())


class Path(NamedTuple):
    cost: int
    head: Node
    nodes: Tuple[Node, ...]


class Graph:
    def __init__(self, grid: np.ndarray):
        self.grid = grid

    @classmethod
    def from_strings(cls, buffer: Iterable[str]):
        arr = []
        for l in buffer:
            arr.append(list(l.strip()))

        grid = np.array(arr)
        return cls(grid)

    def start(self) -> Node:
        x, y = self.grid.shape
        p = Position(x - 2, 1)
        return Node(pos=p, direction=Direction.E)

    def end_pos(self) -> Position:
        x, y = self.grid.shape
        return Position(1, y - 2)

    def is_in(self, n: Node) -> bool:
        xmax, ymax = self.grid.shape
        return (
            (0 <= n.pos.x < xmax)
            and (0 <= n.pos.y < ymax)
            and (self.grid[n.pos] != "#")
        )

    def children(self, n: Node) -> list[Tuple[int, Node]]:
        children = [
            (1, n.forward()),
            (1001, n.left().forward()),
            (1001, n.right().forward()),
        ]
        children = [c for c in children if self.is_in(c[1])]
        return children


def lowest_score(g: Graph) -> int:
    heap = []
    visited = set()

    H.heappush(heap, (0, g.start()))
    endpos = g.end_pos()

    while heap:
        cost, n = H.heappop(heap)
        visited.add(n)

        if n.pos == endpos:
            return cost
        else:
            for c, x in g.children(n):
                if x not in visited:
                    H.heappush(heap, (cost + c, x))

    raise ValueError("No path found")


def part01(pipe: Iterator[str]):
    g = Graph.from_strings(pipe)

    cost = lowest_score(g)
    return cost


def part02(pipe: Iterator[str]):
    g = Graph.from_strings(pipe)

    score = lowest_score(g)
    heap = []
    p0 = Path(head=g.start(), cost=0, nodes=(g.start(),))

    H.heappush(heap, p0)
    endpos = g.end_pos()
    paths = []
    visited_head = dict()

    while heap:
        p = H.heappop(heap)
        visited_head[p.head] = p.cost

        if p.head.pos == endpos:
            paths.append(p)
        else:
            for c, n in g.children(p.head):
                x = Path(p.cost + c, n, p.nodes + (n,))
                v_score = visited_head.get(n, float("inf"))
                if x.cost <= min(score, v_score):
                    H.heappush(heap, x)

    visited = set()
    for p in paths:
        for n in p.nodes:
            visited.add(n.pos)
    return len(visited)


def main():
    p1, p2 = I.tee(sys.stdin, 2)
    print(f"Part01 | {part01(p1)}")
    print(f"Part02 | {part02(p2)}")


if __name__ == "__main__":
    main()
