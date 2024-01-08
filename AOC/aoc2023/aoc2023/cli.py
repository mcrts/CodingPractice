import argparse
import sys
import importlib
import itertools as I

parser = argparse.ArgumentParser()
parser.add_argument('day', type=int, choices=range(1, 11))
parser.add_argument('--part1', action="store_true")
parser.add_argument('--part2', action="store_true")

def main():
    args = parser.parse_args(sys.argv[1:])
    if (not args.part1) and (not args.part2):
        args.part1 = True
        args.part2 = True

    module = importlib.import_module(f'aoc2023.day{args.day:0>2}')
    pipe1, pipe2 = I.tee(sys.stdin, 2)
    if args.part1:
        print(f"Day{args.day:0>2} Part 1 |", module.part1(pipe1))
    if args.part2:
        print(f"Day{args.day:0>2} Part 2 |", module.part2(pipe2))
