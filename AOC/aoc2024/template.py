import itertools as I
import sys
from typing import Iterator


def part01(pipe: Iterator[str]):
    return 0


def part02(pipe: Iterator[str]):
    return 0


def main():
    p1, p2 = I.tee(sys.stdin, 2)
    print(f"Part01 | {part01(p1)}")
    print(f"Part02 | {part02(p2)}")


if __name__ == "__main__":
    main()
