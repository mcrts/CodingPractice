import sys

DELTAS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (1, -1),
    (1, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

def is_symbol(c):
    return not (c.isdigit() or c == ".")

def part1():
    symbols = set()
    parts = set()
    selected_parts = set()
    grid = []
    for i, l in enumerate(sys.stdin):
        l = l.strip()
        grid.append(l)
        symbols_positions = [(i, j) for j, _ in filter(lambda x: is_symbol(x[1]), enumerate(l))]
        symbols = symbols.union(set(symbols_positions))

        parts_positions = [(i, j) for j, _ in filter(lambda x: x[1].isdigit(), enumerate(l))]
        parts = parts.union(set(parts_positions))

        selected_positions = [(i + di, j + dj) for i, j in symbols_positions for di, dj in DELTAS]
        selected_parts = selected_parts.union(set(selected_positions))

    target_parts = parts.difference(selected_parts)
    v = sum([int(grid[i][j]) for i, j in target_parts])
    return v

def part2():
    return 0

def main():
    v = part1()
    print(v)