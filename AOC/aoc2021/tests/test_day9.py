from aoc2021.solver.day09 import find_basin, Point
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


def test_find_bassin():
    arr = INPUT
    p = Point((0, 0), arr, arr[(0, 0)])
    basin_point_sol = Point((1, 0), arr, arr[(1, 0)])
    basin_value, basin_point = find_basin(p)
    assert basin_point == basin_point_sol
    assert basin_value == 3
