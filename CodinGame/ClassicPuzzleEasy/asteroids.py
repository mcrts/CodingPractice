import sys
import numpy as np

w, h, t1, t2, t3 = [int(i) for i in input().split()]
dt = (t3 - t2) / (t2 - t1)

g1 = []
g2 = []
for y in range(h):
    s1, s2 = input().split(" ")
    g1.append(list(s1))
    g2.append(list(s2))

grid1 = np.array(g1, dtype=str, order='F')
grid2 = np.array(g2, dtype=str, order='F')

def grid2coordinate(grid):
    asteroids = dict()
    for idx, x in np.ndenumerate(grid):
        if x != ".":
            asteroids[x] = np.array(idx, dtype=float)
    return asteroids

def coordinate2grid(asteroids, width, height):
    grid = np.full((width, height), fill_value=".", dtype=str, order='F')
    for k, v in sorted(asteroids.items(), reverse=True):
        i, j = v
        if (0 <= i < width) and (0 <= j < height):
            grid[int(i), int(j)] = k
    return grid

def diff(asteroids1, asteroids2):
    asteroids = dict()
    for k, v in asteroids1.items():
        asteroids[k] = asteroids2[k]- v
    return asteroids

def translate(asteroids_0, asteroids_d, dt):
    asteroids = dict()
    for k, v in asteroids_0.items():
        asteroids[k] = v + dt * asteroids_d[k]
    return asteroids

as1 = grid2coordinate(grid1)
as2 = grid2coordinate(grid2)
d = diff(as1, as2)
as3 = translate(as2, d, dt)
grid3 = coordinate2grid(as3, w, h)

print("\n".join(["".join(r) for r in grid3.tolist()]))
