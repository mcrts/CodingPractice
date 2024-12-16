import itertools as I
import sys
from collections import defaultdict
from pprint import pprint
from typing import Iterator


def check_update(rules, update) -> bool:
    for idx, p in enumerate(update):
        children = rules[p]
        for c in children:
            if c in update and update.index(c) <= idx:
                return False
    return True


def reorder(rules, old_update):
    update = list(old_update)
    for idx, p in enumerate(update):
        children = rules[p]
        children = [
            (update.index(c), c)
            for c in children
            if c in update and update.index(c) <= idx
        ]
        if not children:
            continue
        cidx, c = min(children)
        update[cidx] = p
        update[idx] = c
    return update


def part01(pipe: Iterator[str]):
    rules = defaultdict(set)
    for l in pipe:
        if l.strip() == "":
            break
        a, b = l.strip().split("|")
        rules[int(a)].add(int(b))

    count = 0
    for l in pipe:
        update = list(map(int, l.strip().split(",")))
        f = check_update(rules, update)
        if f:
            m = len(update) // 2
            count += update[m]
    return count


def part02(pipe: Iterator[str]):
    rules = defaultdict(set)
    for l in pipe:
        if l.strip() == "":
            break
        a, b = l.strip().split("|")
        rules[int(a)].add(int(b))

    count = 0
    for l in pipe:
        update = list(map(int, l.strip().split(",")))
        if not check_update(rules, update):
            while not check_update(rules, update):
                update = reorder(rules, update)
            m = len(update) // 2
            count += update[m]
    return count
