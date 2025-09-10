import functools as F
import itertools as I
import sys
from pprint import pprint
from typing import Iterator, List, Tuple


def parse_input(pipe: Iterator[str]) -> Tuple[Tuple[str, ...], List[str]]:
    patterns = next(pipe).strip().split(", ")
    next(pipe)
    designs = []
    for l in pipe:
        designs.append(l.strip())
    return tuple(patterns), designs


@F.lru_cache()
def design_is_possible(design: str, patterns: Tuple[str, ...]) -> bool:
    if design == "":
        return True

    children = []
    for p in patterns:
        if design.startswith(p):
            tail = design[len(p) :]
            children.append(tail)

    return any([design_is_possible(c, patterns) for c in children])


@F.lru_cache()
def design_count(design: str, patterns: Tuple[str, ...]) -> int:
    if design == "":
        return 1

    children = []
    for p in patterns:
        if design.startswith(p):
            tail = design[len(p) :]
            children.append(tail)

    children_count = sum([design_count(c, patterns) for c in children])
    return children_count


def part01(pipe: Iterator[str]):
    patterns, designs = parse_input(pipe)
    possible_designs = [design_is_possible(d, patterns) for d in designs]
    return sum(possible_designs)


def part02(pipe: Iterator[str]):
    patterns, designs = parse_input(pipe)
    counts = [design_count(d, patterns) for d in designs]
    return sum(counts)
