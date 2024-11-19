import functools as F
import heapq as H
import itertools as I
import math as M
import re
import sys
from collections import namedtuple
from dataclasses import dataclass, field
from enum import IntEnum, auto
from pprint import pprint
from typing import Any, Iterable, List, Mapping, NamedTuple, Optional, Set, Tuple

import networkx as nx
import numpy as np


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


Direction.OFFSETS = {
    Direction.N: (-1, 0),
    Direction.E: (0, 1),
    Direction.S: (1, 0),
    Direction.W: (0, -1),
}


class Position(NamedTuple):
    x: int
    y: int
    d: Direction

    @classmethod
    def new(cls, x: int, y: int, d: Direction):
        return cls(x, y, d)

    def loc(self) -> np.ndarray:
        return np.array((self.x, self.y))

    def l1_norm(self, other) -> int:
        return np.linalg.norm(self.loc() - other.loc(), ord=1)

    def left(self):
        d = self.d.left()
        dx, dy = Direction.OFFSETS[d]
        return self.new(self.x + dx, self.y + dy, d)

    def right(self):
        d = self.d.right()
        dx, dy = Direction.OFFSETS[d]
        return self.new(self.x + dx, self.y + dy, d)

    def forward(self):
        dx, dy = Direction.OFFSETS[self.d]
        return self.new(self.x + dx, self.y + dy, self.d)


class State(NamedTuple):
    pos: Position
    cost: int
    count: int

    def loc(self) -> np.ndarray:
        return self.pos.loc()


class Grid(NamedTuple):
    grid: np.ndarray
    xmin: int
    ymin: int
    xmax: int
    ymax: int

    @classmethod
    def FromPipe(cls, pipe: Iterable[str]):
        rows = []
        for l in pipe:
            rows.append(list(l.strip()))

        grid = np.array(rows).astype(int)
        xmax, ymax = grid.shape
        return cls(grid, 0, 0, xmax - 1, ymax - 1)

    def start_states(self) -> Iterable[State]:
        s1 = State(Position(0, 0, Direction.E), 0, 0)
        s2 = State(Position(0, 0, Direction.S), 0, 0)
        return s1, s2

    def end_positions(self) -> Iterable[Position]:
        p = (
            Position(self.xmax, self.ymax, Direction.N),
            Position(self.xmax, self.ymax, Direction.E),
            Position(self.xmax, self.ymax, Direction.S),
            Position(self.xmax, self.ymax, Direction.W),
        )
        return p

    def is_in(self, p: Position) -> bool:
        x, y = p.loc()
        return (self.xmin <= x <= self.xmax) and (self.ymin <= y <= self.ymax)

    def get_heat(self, p: Position) -> int:
        return self.grid[tuple(p.loc())]

    def children(self, n: State, minstep: int = 0, maxstep: int = 3) -> List[State]:
        children = []
        left = n.pos.left()
        if self.is_in(left) and n.count >= minstep:
            children.append(State(left, n.cost + self.get_heat(left), 1))

        right = n.pos.right()
        if self.is_in(right) and n.count >= minstep:
            children.append(State(right, n.cost + self.get_heat(right), 1))

        forward = n.pos.forward()
        if self.is_in(forward) and n.count < maxstep:
            children.append(State(forward, n.cost + self.get_heat(forward), n.count + 1))

        return children


@dataclass(order=True)
class PrioritizedState:
    priority: int
    state: State = field(compare=False)


def implicit_dijkstra(
    grid: Grid,
    sources: Iterable[State],
    targets: Set[Position],
    minstep: int = 0,
    maxstep: int = 3,
) -> int:
    seen: Set[State] = set()
    queue: List[PrioritizedState] = []

    for s in sources:
        H.heappush(queue, PrioritizedState(s.cost, s))
        seen.add((s.pos, s.count))

    while queue:
        pstate = H.heappop(queue)
        s = pstate.state
        if s.pos in targets and (minstep < s.count < maxstep):
            return s

        for c in grid.children(s, minstep, maxstep):
            if (c.pos, c.count) not in seen:
                H.heappush(queue, PrioritizedState(c.cost, c))
                seen.add((c.pos, c.count))

    return -1


def implicit_astar(
    grid: Grid,
    sources: Iterable[State],
    targets: Set[Position],
    minstep: int = 0,
    maxstep: int = 3,
) -> int:
    seen: Set[State] = set()
    queue: List[PrioritizedState] = []
    t = next(iter(targets))

    for s in sources:
        h = s.cost + t.l1_norm(s.pos)
        H.heappush(queue, PrioritizedState(h, s))
        seen.add((s.pos, s.count))

    while queue:
        pstate = H.heappop(queue)
        s = pstate.state
        if s.pos in targets and (minstep <= s.count < maxstep):
            return s

        for c in grid.children(s, minstep, maxstep):
            if (c.pos, c.count) not in seen:
                h = c.cost + t.l1_norm(c.pos)
                H.heappush(queue, PrioritizedState(h, c))
                seen.add((c.pos, c.count))

    return -1


def part1(pipe):
    g = Grid.FromPipe(pipe)
    s = g.start_states()
    t = set(g.end_positions())
    r = implicit_astar(g, s, t, 0, 3)
    return r.cost


def part2(pipe):
    g = Grid.FromPipe(pipe)
    s = g.start_states()
    t = set(g.end_positions())
    r = implicit_astar(g, s, t, 4, 10)
    return r.cost
