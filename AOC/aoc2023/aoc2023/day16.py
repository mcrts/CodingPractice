import sys
import re

import itertools as I
import functools as F
from collections import namedtuple
from enum import Enum
from pprint import pprint

import numpy as np
import networkx as nx

class Tile(Enum):
    MIRROR_R = '/'
    MIRROR_L = '\\'
    SPLITTER_V = '|'
    SPLITTER_H = '-'
    EMPTY = '.'
    
class Direction(Enum):
    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
    DOWN = 'down'

Node = namedtuple("Node", ["x", "y", "d"])
class Node(Node):
    @classmethod
    def OutsideNode(cls):
        return cls(None, None, None)
    
    def idx(self):
        return self.x, self.y


def go_straight(grid, n: Node):
    xmax, ymax = grid.shape
    is_top_border = n.x == 0
    is_bottom_border = n.x == xmax-1
    is_left_border = n.y == 0
    is_right_border = n.y == ymax-1

    match n.d, is_top_border, is_bottom_border, is_left_border, is_right_border:
        case Direction.UP, True, _, _, _:
            return Node.OutsideNode()
        case Direction.UP, False, _, _, _:
            return Node(n.x - 1, n.y, n.d)
        case Direction.DOWN, _, True, _, _:
            return Node.OutsideNode()
        case Direction.DOWN, _, False, _, _:
            return Node(n.x + 1, n.y, n.d)
        case Direction.LEFT, _, _, True, _:
            return Node.OutsideNode()
        case Direction.LEFT, _, _, False, _:
            return Node(n.x, n.y - 1, n.d)
        case Direction.RIGHT, _, _, _, True:
            return Node.OutsideNode()
        case Direction.RIGHT, _, _, _, False:
            return Node(n.x, n.y + 1, n.d)
    return n


def get_children(grid, n: Node):
    children = set()
    t = Tile(grid[n.idx()])
    match (t, n.d):
        case Tile.MIRROR_R, Direction.RIGHT:
            c = Node(n.x, n.y, Direction.UP)
            children = {go_straight(grid, c)}
        case Tile.MIRROR_R, Direction.LEFT:
            c = Node(n.x, n.y, Direction.DOWN)
            children = {go_straight(grid, c)}
        case Tile.MIRROR_R, Direction.UP:
            c = Node(n.x, n.y, Direction.RIGHT)
            children = {go_straight(grid, c)}
        case Tile.MIRROR_R, Direction.DOWN:
            c = Node(n.x, n.y, Direction.LEFT)
            children = {go_straight(grid, c)}

        case Tile.MIRROR_L, Direction.RIGHT:
            c = Node(n.x, n.y, Direction.DOWN)
            children = {go_straight(grid, c)}
        case Tile.MIRROR_L, Direction.LEFT:
            c = Node(n.x, n.y, Direction.UP)
            children = {go_straight(grid, c)}
        case Tile.MIRROR_L, Direction.UP:
            c = Node(n.x, n.y, Direction.LEFT)
            children = {go_straight(grid, c)}
        case Tile.MIRROR_L, Direction.DOWN:
            c = Node(n.x, n.y, Direction.RIGHT)
            children = {go_straight(grid, c)}

        case Tile.SPLITTER_V, (Direction.UP | Direction.DOWN):
            children = {go_straight(grid, n)}
        case Tile.SPLITTER_V, (Direction.LEFT | Direction.RIGHT):
            children = {
                Node(n.x, n.y, Direction.UP),
                Node(n.x, n.y, Direction.DOWN)
            }
        case Tile.SPLITTER_H, (Direction.LEFT | Direction.RIGHT):
            children = {go_straight(grid, n)}
        case Tile.SPLITTER_H, (Direction.UP | Direction.DOWN):
            children = {
                Node(n.x, n.y, Direction.LEFT),
                Node(n.x, n.y, Direction.RIGHT)
            }
        case Tile.EMPTY, _:
            children = {go_straight(grid, n)}
        case  _:
            raise Exception(f"unable to match {((t, n))}")
    
    return children


def build_graph(grid, st: Node):
    g = nx.DiGraph()
    g.add_node(st)
    frontier = set([st])

    while frontier:
        n = frontier.pop()
        if n == Node.OutsideNode():
            continue

        children = get_children(grid, n)
        for c in children:
            if c not in g:
                g.add_node(c)
                frontier.add(c)
            g.add_edge(n, c)

    return g

def build_graph2(grid, starts):
    g = nx.DiGraph()
    for st in starts:
        g.add_node(st)

    frontier = set(starts)

    while frontier:
        n = frontier.pop()
        if n == Node.OutsideNode():
            continue

        children = get_children(grid, n)
        for c in children:
            if c not in g:
                g.add_node(c)
                frontier.add(c)
            g.add_edge(n, c)

    return g


def part1(pipe):
    rows = []
    for l in pipe:
        rows.append(list(l.strip()))
    
    grid = np.array(rows)
    st = Node(0, 0, Direction.RIGHT)
    g = build_graph(grid, st)

    visited = set()
    frontier = set(g.predecessors(Node.OutsideNode()))
    
    while frontier:
        n = frontier.pop()
        visited.add(n)
        children = set(g.predecessors(n))
        unv_children = children.difference(visited)
        frontier = frontier.union(unv_children)
    
    visited_positions = set((n.idx() for n in visited))

    return len(visited_positions)

def part2(pipe):
    rows = []
    for l in pipe:
        rows.append(list(l.strip()))
    
    grid = np.array(rows)
    xmax, ymax = grid.shape
    starts = []
    starts.extend([Node(0, i, Direction.DOWN) for i in range(0, ymax)])
    starts.extend([Node(xmax-1, i, Direction.UP) for i in range(0, ymax)])
    starts.extend([Node(i, ymax-1, Direction.LEFT) for i in range(0, xmax)])
    starts.extend([Node(i, 0, Direction.RIGHT) for i in range(0, xmax)])

    g = build_graph2(grid, starts)

    frontier = set([Node.OutsideNode()])
    property_trail = dict()
    property_trail[Node.OutsideNode()] = set()
    
    while frontier:
        n = frontier.pop()
        n_trail = property_trail.get(n)

        children = set(g.predecessors(n))
        for c in children:
            c_trail = property_trail.get(c, set())
            new_c_trail = n_trail.union(set([c.idx()]))
            if new_c_trail - c_trail:
                property_trail[c] = c_trail.union(new_c_trail)
                frontier.add(c)
    
    r = max([len(property_trail[s]) for s in starts])

    return r
