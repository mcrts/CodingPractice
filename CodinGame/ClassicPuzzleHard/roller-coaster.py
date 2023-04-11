import sys
import math

def debug(*args):
    print(*args, file=sys.stderr, flush=True)


def greedy(l, c, groups):
    dirham = 0
    for _ in range(c):
        cart = list()
        while groups and (sum(cart) + groups[0] <= l):
            cart.append(groups.pop(0))
        groups.extend(cart)
        dirham += sum(cart)
    return dirham


l, c, n = [int(i) for i in input().split()]
groups = list()
for i in range(n):
    pi = int(input())
    groups.append(pi)

res = greedy(l, c, groups)
debug(res)
print(res)
