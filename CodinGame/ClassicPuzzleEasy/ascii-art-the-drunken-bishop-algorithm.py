import sys
import math

from functools import reduce

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
HEXMAP = {
    "0": ("00", "00"),
    "1": ("01", "00"),
    "2": ("10", "00"),
    "3": ("11", "00"),
    "4": ("00", "01"),
    "5": ("01", "01"),
    "6": ("10", "01"),
    "7": ("11", "01"),
    "8": ("00", "10"),
    "9": ("01", "10"),
    "a": ("10", "10"),
    "b": ("11", "10"),
    "c": ("00", "11"),
    "d": ("01", "11"),
    "e": ("10", "11"),
    "f": ("11", "11"),
}

BISHOPMAP = [" ", ".", "o", "+", "=", "*", "B", "O", "X", "@", "%", "&", "#", "/", "^"]


class Board:
    def __init__(self):
        self.array2D = [[0 for _ in range(17)] for _ in range(9)]
        self.bishop = (4, 8)
        self.start = (4, 8)

    def __str__(self):
        array = [list(map(lambda i: BISHOPMAP[(i % 15)], row)) for row in self.array2D]
        y, x = self.bishop
        array[y][x] = "E"
        y, x = self.start
        array[y][x] = "S"

        string_array = []
        string_array.append("+---[CODINGAME]---+")
        for row in array:
            string_array.append("|" + "".join(map(str, row)) + "|")
        string_array.append("+-----------------+")
        return "\n".join(string_array)

    def handle_topleft(self):
        y, x = self.bishop
        if y == 0 and x == 0:
            pass
        elif y == 0:
            self.bishop = (y, x - 1)
        elif x == 0:
            self.bishop = (y - 1, x)
        else:
            self.bishop = (y - 1, x - 1)
        y, x = self.bishop
        self.array2D[y][x] += 1

    def handle_topright(self):
        y, x = self.bishop
        if y == 0 and x == 16:
            pass
        elif y == 0:
            self.bishop = (y, x + 1)
        elif x == 16:
            self.bishop = (y - 1, x)
        else:
            self.bishop = (y - 1, x + 1)
        y, x = self.bishop
        self.array2D[y][x] += 1

    def handle_bottomleft(self):
        y, x = self.bishop
        if y == 8 and x == 0:
            pass
        elif y == 8:
            self.bishop = (y, x - 1)
        elif x == 0:
            self.bishop = (y + 1, x)
        else:
            self.bishop = (y + 1, x - 1)
        y, x = self.bishop
        self.array2D[y][x] += 1

    def handle_bottomright(self):
        y, x = self.bishop
        if y == 8 and x == 16:
            pass
        elif y == 8:
            self.bishop = (y, x + 1)
        elif x == 16:
            self.bishop = (y + 1, x)
        else:
            self.bishop = (y + 1, x + 1)
        y, x = self.bishop
        self.array2D[y][x] += 1

    def parse_fingerprint(self, fingerprint):
        actions = reduce(
            tuple.__add__,
            map(
                HEXMAP.get,
                reduce(
                    str.__add__,
                    map(
                        lambda x: x[::-1],
                        fingerprint.split(":"),
                    ),
                ),
            ),
        )

        return actions

    def solve(self, actions):
        for action in actions:
            if action == "00":
                self.handle_topleft()
            elif action == "01":
                self.handle_topright()
            elif action == "10":
                self.handle_bottomleft()
            elif action == "11":
                self.handle_bottomright()
            else:
                raise ValueError("unhandle action", action)


fingerprint = input()
board = Board()
actions = board.parse_fingerprint(fingerprint)
board.solve(actions)

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print(board)
