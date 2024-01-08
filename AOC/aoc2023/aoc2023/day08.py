import sys
import re
import math

import itertools as I
import functools as F
from collections import namedtuple
from pprint import pprint

RE_NODE = r"^(?P<src>\w{3}) = \((?P<l>\w{3}), (?P<r>\w{3})\)$"
Node = namedtuple("Node", ["src", 'l', 'r'])

def part1(buffer):
    instructions = I.cycle(next(buffer).strip())
    graph = dict()
    next(buffer)
    for l in buffer:
        m = re.match(RE_NODE, l)
        n = Node(**m.groupdict())
        graph[n.src] = n

    n = graph['AAA']
    c = 0
    while n.src != 'ZZZ':
        c += 1
        instr = next(instructions)
        match instr:
            case 'L':
                n = graph[graph[n.src].l]
            case 'R':
                n = graph[graph[n.src].r]
    return c

def part2(buffer):
    def move(graph, instructions, node):
        c = 0
        N = len(instructions)
        idx = 0
        while c == 0 or not node.src.endswith("Z"):
            instr = instructions[idx]
            match instr:
                case 'L':
                    node = graph[graph[node.src].l]
                case 'R':
                    node = graph[graph[node.src].r]
            c += 1
            idx = (idx + 1) % N
        return c

    def lcm(a, b):
        return abs(a*b) // math.gcd(a, b)
        
    instructions = next(buffer).strip()
    graph = dict()
    next(buffer)
    for l in buffer:
        m = re.match(RE_NODE, l)
        n = Node(**m.groupdict())
        graph[n.src] = n

    nodes = [v for k, v in graph.items() if k.endswith("A")]
    steps = [move(graph, instructions, n) for n in nodes]
    c = F.reduce(lcm, steps)

    return c