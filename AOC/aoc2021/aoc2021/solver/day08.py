from typing import Iterator, Any, Sequence, Tuple
import itertools as it
from bidict import bidict

from aoc2021.utils import Solver, input_path

DAY = 8
INPATH = input_path(DAY)


def lineparser(instream: str) -> Tuple[list[frozenset[str]], list[frozenset[str]]]:
    inputs, outputs = instream.split("|", 2)
    inputs = [frozenset(s) for s in inputs.strip().split(" ")]
    outputs = [frozenset(s) for s in outputs.strip().split(" ")]
    return inputs, outputs


def lineparser_solver1(instream: str) -> int:
    _, outputs = lineparser(instream)
    easy_digs = [o for o in outputs if len(o) in (2, 4, 3, 7)]
    return len(easy_digs)


def digits_encoder_decoder(inputs: list[frozenset[str]]) -> bidict:
    digits_candidate = {
        0: set([s for s in inputs if len(s) == 6]),
        1: set([s for s in inputs if len(s) == 2]),
        2: set([s for s in inputs if len(s) == 5]),
        3: set([s for s in inputs if len(s) == 5]),
        4: set([s for s in inputs if len(s) == 4]),
        5: set([s for s in inputs if len(s) == 5]),
        6: set([s for s in inputs if len(s) == 6]),
        7: set([s for s in inputs if len(s) == 3]),
        8: set([s for s in inputs if len(s) == 7]),
        9: set([s for s in inputs if len(s) == 6]),
    }
    digits_code = bidict(
        {
            1: digits_candidate[1].pop(),
            4: digits_candidate[4].pop(),
            7: digits_candidate[7].pop(),
            8: digits_candidate[8].pop(),
        }
    )
    digits_candidate[3] = set(s for s in digits_candidate[3] if digits_code[1] < s)
    digits_code[3] = digits_candidate[3].pop()
    digits_candidate[2].remove(digits_code[3])
    digits_candidate[5].remove(digits_code[3])

    digits_candidate[6] = set(s for s in digits_candidate[6] if not digits_code[1] < s)
    digits_code[6] = digits_candidate[6].pop()
    digits_candidate[0].remove(digits_code[6])
    digits_candidate[9].remove(digits_code[6])

    digits_candidate[5] = set(s for s in digits_candidate[5] if s < digits_code[6])
    digits_code[5] = digits_candidate[5].pop()
    digits_candidate[2].remove(digits_code[5])
    digits_code[2] = digits_candidate[2].pop()

    digits_candidate[9] = set(s for s in digits_candidate[9] if digits_code[5] < s)
    digits_code[9] = digits_candidate[9].pop()
    digits_candidate[0].remove(digits_code[9])
    digits_code[0] = digits_candidate[0].pop()

    return digits_code


def lineparser_solver2(instream: str) -> int:
    inputs, outputs = lineparser(instream)
    digits_coder = digits_encoder_decoder(inputs)
    res = int("".join([str(digits_coder.inv[o]) for o in outputs]), base=10)
    return res


solver01 = Solver(
    lineparser=lineparser_solver1,
    parser=sum,  # type: ignore
    solver=lambda t: t,  # type: ignore
)

solver02 = Solver(
    lineparser=lineparser_solver2,
    parser=sum,  # type: ignore
    solver=lambda t: t,  # type: ignore
)


def main():
    print(f"Day {DAY:02d} - Part01 :", solver01.solve(INPATH))
    print(f"Day {DAY:02d} - Part02 :", solver02.solve(INPATH))
