import itertools as it
from typing import Iterator, Sequence, Tuple, Self
from pydantic import BaseModel

from aoc2021.utils import Solver, input_path


INPATH = input_path(4)


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


def solve_part1(parsed_input: Tuple[Iterator[int], Sequence[BingoBoard]]) -> int:
    draws, boards = parsed_input
    for d in draws:
        boards = [b.apply_draw(d) for b in boards]
        wins = [b.win() for b in boards]
        if any(wins):
            board = boards[wins.index(True)]
            score = board.score() * d
            return score
    return 0


def solve_part2(parsed_input: Tuple[Iterator[int], Sequence[BingoBoard]]) -> int:
    draws, boards = parsed_input
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


solver01 = Solver(
    parser=parse_input,  # type: ignore
    solver=solve_part1,  # type: ignore
)

solver02 = Solver(
    parser=parse_input,  # type: ignore
    solver=solve_part2,  # type: ignore
)


def main():
    print("Day 04 - Part01 :", solver01.solve(INPATH))
    print("Day 04 - Part02 :", solver02.solve(INPATH))
