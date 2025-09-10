import itertools as I
import sys
from pprint import pprint
from typing import Iterator

import numpy as np
import regex as re

RE_XMAS = re.compile(r"(?=(XMAS|SAMX))")
RE_MAS = re.compile(r"(?=(MAS|SAM))")


def part01(pipe: Iterator[str]):
    grid = []
    for line in pipe:
        grid.append(list(line.strip()))
    hgrid = np.array(grid)
    vgrid = np.rot90(hgrid)

    count = 0
    for row in hgrid:
        l = "".join(row)
        c = len(RE_XMAS.findall(l))
        count += c

    for row in vgrid:
        l = "".join(row)
        c = len(RE_XMAS.findall(l))
        count += c

    offset_row = 1 - hgrid.shape[0]
    offset_column = hgrid.shape[1]
    for offset in range(offset_row, offset_column):
        row = hgrid.diagonal(offset=offset)
        l = "".join(row)
        c = len(RE_XMAS.findall(l))
        count += c

    offset_row = 1 - vgrid.shape[0]
    offset_column = vgrid.shape[1]
    for offset in range(offset_row, offset_column):
        row = vgrid.diagonal(offset=offset)
        l = "".join(row)
        c = len(RE_XMAS.findall(l))
        count += c

    return count


def part02(pipe: Iterator[str]):
    grid = []
    for line in pipe:
        grid.append(list(line.strip()))
    hgrid = np.array(grid)

    count = 0
    points = np.argwhere(hgrid == "A")
    for ix, iy in points:
        cell = hgrid[ix - 1 : ix + 2, iy - 1 : iy + 2]
        if cell.shape != (3, 3):
            continue
        else:
            d0 = "".join(cell.diagonal(0))
            d1 = "".join(np.rot90(cell).diagonal(0))
            flag = (d0 in ("MAS", "SAM")) and (d1 in ("MAS", "SAM"))
            count += flag
    return count
