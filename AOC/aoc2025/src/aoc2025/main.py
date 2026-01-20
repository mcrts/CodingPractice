import argparse
import importlib
import itertools as I
import os
import shutil
import sys
from pathlib import Path

DIR_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
TEMPLATE = DIR_PATH / "day.template"
FILES = DIR_PATH / "files"
TESTFILES = DIR_PATH / "test_files"

parser = argparse.ArgumentParser()
parser.add_argument("day", type=int, choices=range(1, 26))
parser.add_argument("-i", "--input", type=Path)
parser.add_argument("--part1", action="store_true")
parser.add_argument("--part2", action="store_true")
parser.add_argument("--test", action="store_true")


def main():
    args = parser.parse_args(sys.argv[1:])
    if args.test and args.input:
        parser.error(f"-i and --test cannot be both set.")

    if (not args.part1) and (not args.part2):
        args.part1 = True
        args.part2 = True

    if args.input:
        pass
    elif args.test:
        args.input = TESTFILES / f"day{args.day:0>2}.txt"
    else:
        args.input = FILES / f"day{args.day:0>2}.txt"

    module = importlib.import_module(f"aoc2025.day{args.day:0>2}")
    pipe1, pipe2 = I.tee(args.input.open("r").readlines(), 2)
    if args.part1:
        print(f"Day{args.day:0>2} Part 1 |", module.part1(pipe1))
    if args.part2:
        print(f"Day{args.day:0>2} Part 2 |", module.part2(pipe2))


def template():
    day = int(sys.argv[1])
    shutil.copyfile(TEMPLATE, DIR_PATH / f"day{day:02}.py")
    open(FILES / f"day{day:02}.txt", "a").close()
    open(TESTFILES / f"day{day:02}.txt", "a").close()
