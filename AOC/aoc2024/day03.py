import itertools as I
import re
import sys
from typing import Iterator

RE_MUL = r"mul\((\d+),(\d+)\)"
RE_DO = r"do\(\)"
RE_DONT = r"don't\(\)"


def part01(pipe: Iterator[str]):
    count = 0
    for line in pipe:
        l = line.strip()
        matches = re.finditer(RE_MUL, l)
        for m in matches:
            a, b = m.groups()
            count += int(a) * int(b)
    return count


def part02(pipe: Iterator[str]):
    count = 0
    flag = True
    pattern = re.compile("%s|%s|%s" % (RE_MUL, RE_DO, RE_DONT))

    for line in pipe:
        l = line.strip()
        matches = pattern.finditer(l)
        for m in matches:
            instr = m.group()
            if instr == "do()":
                flag = True
            elif instr == "don't()":
                flag = False
            elif instr.startswith("mul"):
                if flag:
                    a, b = m.groups()
                    count += int(a) * int(b)
            else:
                raise ValueError("unhandled case", instr)
    return count


def main():
    p1, p2 = I.tee(sys.stdin, 2)
    print(f"Part01 | {part01(p1)}")
    print(f"Part02 | {part02(p2)}")


if __name__ == "__main__":
    main()
