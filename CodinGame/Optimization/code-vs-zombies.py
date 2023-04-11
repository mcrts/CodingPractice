import sys
import math
import numpy as np

def debug(*args):
    print(*args, file=sys.stderr, flush=True)

ASH_SPD = 1000
Z_SPD = 400
ASH_RAD = 2000
Z_RAD = 400


def is_saveable(player, human, zombies):
    t_ash = math.ceil(
        (np.linalg.norm(player - human) - ASH_RAD) / ASH_SPD
    )
    f_t_zombie = lambda z: math.ceil(
        (np.linalg.norm(z - human) - Z_RAD) / Z_SPD
    )
    f_filter = lambda z: t_ash - 1 > f_t_zombie(z)
    zombies = filter(f_filter, zombies.values())
    return len(list(zombies)) == 0

def attack(player, humans, zombies):
    t = next(iter(zombies.values()))
    return t

def defend_first(player, humans, zombies):
    t = next(iter(humans.values()))
    return t

def defend_closest(player, humans, zombies):
    f_dist = lambda x: np.linalg.norm(x - player)
    humans_pos = sorted(humans.values(), key=f_dist)
    return humans_pos[0]

def defend_closest_saveable(player, humans, zombies):
    humans = humans.values()
    humans = filter(lambda h: is_saveable(player, h, zombies), humans)
    f_dist = lambda x: np.linalg.norm(x - player)
    humans = sorted(humans, key=f_dist)
    return humans[0]

# game loop
while True:
    x, y = [int(i) for i in input().split()]
    player = np.array((x, y), dtype=int)
    human_count = int(input())
    humans = dict()
    for _ in range(human_count):
        i, x, y = [int(j) for j in input().split()]
        humans[i] = np.array((x, y), dtype=int)
    
    zombie_count = int(input())
    zombies = dict()
    for i in range(zombie_count):
        i, x, y, _, _ = [int(j) for j in input().split()]
        zombies[i] = np.array((x, y), dtype=int)

    target = defend_closest_saveable(player, humans, zombies)

    print(f"{target[0]} {target[1]}")

