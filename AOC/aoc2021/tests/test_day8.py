from aoc2021.solver.day08 import digits_encoder_decoder

from bidict import bidict


def test_digits_coder():
    inputs = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab"
    encoded = [frozenset(s) for s in inputs.split(" ")]
    digits_coder = digits_encoder_decoder(encoded)
    solution_coder = bidict(
        {
            0: frozenset("cagedb"),
            1: frozenset("ab"),
            2: frozenset("gcdfa"),
            3: frozenset("fbcad"),
            4: frozenset("eafb"),
            5: frozenset("cdfbe"),
            6: frozenset("cdfgeb"),
            7: frozenset("dab"),
            8: frozenset("acedgfb"),
            9: frozenset("cefabd"),
        }
    )
    assert digits_coder == solution_coder


def test_case01():
    encoded = [
        frozenset({"a", "b", "f", "e", "d", "g"}),
        frozenset({"b", "c", "e", "d", "g"}),
        frozenset({"b", "c", "g"}),
        frozenset({"c", "g"}),
        frozenset({"a", "b", "c", "f", "e", "d", "g"}),
        frozenset({"b", "f", "e", "d", "g"}),
        frozenset({"a", "b", "c", "f", "d", "g"}),
        frozenset({"a", "b", "c", "e", "d"}),
        frozenset({"b", "c", "f", "e", "d", "g"}),
        frozenset({"c", "g", "f", "e"}),
    ]
    digits_coder = digits_encoder_decoder(encoded)
    solution_coder = bidict(
        {
            1: frozenset({"c", "g"}),
            4: frozenset({"c", "f", "g", "e"}),
            7: frozenset({"c", "b", "g"}),
            8: frozenset({"g", "b", "a", "c", "d", "f", "e"}),
            3: frozenset({"g", "b", "d", "c", "e"}),
            6: frozenset({"g", "b", "a", "d", "f", "e"}),
            5: frozenset({"g", "b", "d", "f", "e"}),
            2: frozenset({"b", "a", "d", "c", "e"}),
            9: frozenset({"g", "b", "c", "d", "f", "e"}),
            0: frozenset({"g", "b", "a", "c", "d", "f"}),
        }
    )
    assert digits_coder == solution_coder
