import os
from pathlib import Path
import itertools as it
from typing import Callable, Iterable, Iterator, TypeVar, Tuple

from pydantic import BaseModel


DIR_PATH = Path(os.path.dirname(__file__))


def input_path(day: int) -> Path:
    return DIR_PATH / "inputs" / f"day{day:02d}.txt"


def stream_from_text(input_path: Path) -> Iterator[str]:
    with open(input_path, "r", buffering=1, encoding="utf-8") as f:
        for l in f:
            yield l.strip()


T = TypeVar("T")
ParsedLine = TypeVar("ParsedLine")


class Solver(BaseModel):
    lineparser: Callable[[str], ParsedLine] = lambda s: s  # type: ignore
    parser: Callable[[Iterator[ParsedLine]], T]  # type: ignore
    solver: Callable[[T], int]  # type: ignore

    def solve(self, input_path: Path) -> int:
        instream = stream_from_text(input_path)
        instream = (self.lineparser(s) for s in instream)
        state = self.parser(instream)
        result = self.solver(state)
        return result
