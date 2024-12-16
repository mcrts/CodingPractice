from collections import namedtuple
from enum import IntEnum, auto
from pprint import pprint
from typing import Iterable, Tuple


def expand(report: Iterable[int]) -> Iterable[str]:
    blockid = 0
    expanded_report = []
    is_file = True
    for i in report:
        if is_file:
            expanded_report.extend([str(blockid)] * i)
            blockid += 1
        else:
            expanded_report.extend(["."] * i)
        is_file = not is_file
    return expanded_report


def compress_frag(report: Iterable[str]) -> Iterable[str]:
    r = list(report)
    i = 0
    j = len(r) - 1
    while i < j:
        if r[i] != ".":
            i += 1
        elif r[j] == ".":
            j -= 1
        else:
            r[i], r[j] = r[j], r[i]
            i += 1
            j -= 1
    return r


def part1(pipe: Iterable[str]) -> int:
    report = list(map(int, next(pipe).strip()))
    report = expand(report)
    report = compress_frag(report)

    count = 0
    for i, v in enumerate(report):
        if v != ".":
            count += i * int(v)
    return count


class BlockKind(IntEnum):
    File = auto()
    Free = auto()


Block = namedtuple("Block", ["kind", "blockid", "len", "offset"])


def map_disk(report: Iterable[int]) -> Iterable[Block]:
    blocks = []

    is_file = True
    offset = 0
    block_id = 0
    for i in report:
        if is_file:
            block = Block(BlockKind.File, block_id, i, offset)
            blocks.append(block)
            block_id += 1
            offset += i
        else:
            block = Block(BlockKind.Free, -1, i, offset)
            blocks.append(block)
            offset += i
        is_file = not is_file
    return blocks


def move(blocks: Iterable[Block], t: Block):
    free_blocks = [
        (i, b)
        for i, b in enumerate(blocks)
        if b.len <= t.len and b.kind == BlockKind.Free and b.offset < t.offset
    ]
    if free_blocks:
        i, free_block = free_blocks[0]
        new_t = Block(BlockKind.File, t.block_id, t.len, free_block.offset)
        blocks[i] = new_t


def part2(pipe: Iterable[str]) -> int:
    report = list(map(int, next(pipe).strip()))
    blocks = map_disk(report)

    new_blocks = list(blocks)

    for b in blocks[::-1]:
        if b.kind == BlockKind.File:
            move(new_blocks, b)

    return 0
