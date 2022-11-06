import os
import itertools as it
from pathlib import Path
from typing import Generator, Iterable, Iterator, Sequence, Tuple, Self

from pydantic import BaseModel

from aoc2021.utils import stream_from_text

DIR_PATH = os.path.dirname(__file__)
INPATH = Path(DIR_PATH) / "input.txt"
DAY = "04"


class BingoBoard(BaseModel):
    numbers: list[int] = []
    marks: list[bool] = [False for _ in range(5 * 5)]

    def apply_draw(self, draw: int) -> Self:
        board = self.copy()
        if draw in self.numbers:
            idx = self.numbers.index(draw)
            board.marks[idx] = True
        return board

    def check_col(self, idx: int) -> bool:
        row = filter(lambda t: t[0] % 5 == idx, enumerate(self.marks))
        check = all(map(lambda t: t[1], row))
        return check

    def check_row(self, idx: int) -> bool:
        row = filter(lambda t: t[0] // 5 == idx, enumerate(self.marks))
        check = all(map(lambda t: t[1], row))
        return check

    def win(self) -> bool:
        for i in range(5):
            check = self.check_col(i)
            if check:
                return True
            check = self.check_row(i)
            if check:
                return True
        return False

    def score(self) -> int:
        return sum(it.compress(self.numbers, map(lambda x: not x, self.marks)))


def parse_input(instream: Iterator[str]) -> Tuple[Iterator[int], Sequence[BingoBoard]]:
    draw = map(int, next(instream).split(","))
    next(instream)
    boards = ()
    lines = []
    stream = map(
        lambda s: tuple(map(int, filter(bool, s.replace("  ", " ").split(" ")))),
        instream,
    )
    for line in stream:
        if not line:
            boards += (BingoBoard(numbers=lines),)
            lines = []
            continue
        else:
            lines.extend(line)
    boards += (BingoBoard(numbers=lines),)
    return draw, boards


def solve_part1(instream: Iterator[str]) -> int:
    draws, boards = parse_input(instream)

    for d in draws:
        boards = [b.apply_draw(d) for b in boards]
        wins = [b.win() for b in boards]
        if any(wins):
            board = boards[wins.index(True)]
            score = board.score() * d
            return score
    return 0


def solve_part2(instream: Iterator[str]) -> int:
    draws, boards = parse_input(instream)

    for d in draws:
        boards = [b.apply_draw(d) for b in boards]
        newboards = [b for b in boards if not b.win()]
        if len(newboards) == 0:
            board = boards[0]
            score = board.score() * d
            return score
        else:
            boards = newboards
    return 0


def main():
    stream = stream_from_text(INPATH)
    print(
        f"Day {DAY} - Part01 : {solve_part1(stream)}",
    )

    stream = stream_from_text(INPATH)
    print(
        f"Day {DAY} - Part02 : {solve_part2(stream)}",
    )
