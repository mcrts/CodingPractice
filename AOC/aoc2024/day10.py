import itertools as I
import sys
from pprint import pprint
from typing import Iterator, Tuple

import networkx as nx
import numpy as np

Coordinate2D = Tuple[int, int]


def parse_input(pipe: Iterator[str]) -> np.ndarray:
    grid = []
    for l in pipe:
        grid.append(list(map(int, list(l.strip()))))
    return np.array(grid)


def grid_neighbours(grid: np.ndarray, idx: Coordinate2D) -> list[Coordinate2D]:
    h = grid[idx]
    ymax, xmax = grid.shape
    y, x = idx
    indices = [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]
    indices = [(j, i) for (j, i) in indices if 0 <= j < ymax and 0 <= i < xmax]
    indices = [x for x in indices if grid[x] - h == 1]
    return indices


def make_graph(grid: np.ndarray) -> nx.DiGraph:
    g = nx.DiGraph()
    for idx, v in np.ndenumerate(grid):
        g.add_node(idx, h=v)

    for idx, v in np.ndenumerate(grid):
        neighbours = grid_neighbours(grid, idx)
        for nidx in neighbours:
            g.add_edge(idx, nidx)
    return g


def part01(pipe: Iterator[str]):
    grid = parse_input(pipe)
    g = make_graph(grid)

    start_nodes = [n for n, d in g.nodes(data=True) if d["h"] == 0]
    end_nodes = [n for n, d in g.nodes(data=True) if d["h"] == 9]
    count = 0
    for s in start_nodes:
        for t in end_nodes:
            count += nx.algorithms.has_path(g, s, t)

    return count


def part02(pipe: Iterator[str]):
    grid = parse_input(pipe)
    g = make_graph(grid)

    start_nodes = [n for n, d in g.nodes(data=True) if d["h"] == 0]
    end_nodes = [n for n, d in g.nodes(data=True) if d["h"] == 9]
    count = 0
    for s in start_nodes:
        for t in end_nodes:
            paths = nx.algorithms.all_simple_paths(g, s, t)
            count += len(list(paths))
    return count
