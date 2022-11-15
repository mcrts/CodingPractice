from aoc2021.solver.day09 import find_basin, Point, Heatmap
import numpy as np

INPUT = np.vstack(
    [
        [2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
        [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
        [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
        [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
        [9, 8, 9, 9, 9, 6, 5, 6, 7, 8],
    ]
)
HEATMAP = INPUT.view(Heatmap)


def test_find_bassin():
    p = Point((0, 0), HEATMAP, HEATMAP[(0, 0)])
    assert find_basin(p) == (0, 1)
