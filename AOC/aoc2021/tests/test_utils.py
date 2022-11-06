import pytest

from aoc2021 import utils
from aoc2021.inputs import DAYS_IMPLEMENTED


@pytest.mark.parametrize("day", range(1, DAYS_IMPLEMENTED + 1))
def test_input_path_exists(day):
    assert utils.input_path(day).exists()


@pytest.mark.parametrize("day", range(1, DAYS_IMPLEMENTED + 1))
def test_input_path_as_content(day):
    with open(utils.input_path(day), "r") as f:
        content = f.read()
    print(content)
    assert content


def test_solver_linecount():
    """Count line of Day01 input"""
    inpath = utils.input_path(1)
    solver = utils.Solver(parser=lambda s: map(lambda _: 1, s), solver=sum)  # type: ignore
    assert solver.solve(inpath) == 2000


def test_solver_charcount():
    """Count characters of Day01 input"""
    inpath = utils.input_path(1)
    solver = utils.Solver(
        lineparser=len,
        parser=list,
        solver=sum,  # type: ignore
    )

    assert solver.solve(inpath) == 7696
