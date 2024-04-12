import sys
from collections import namedtuple
import re
import functools as F

RE_GAME = r"^Game (?P<id>\d+)"
RE_TURN = "|".join([
    r"(?P<green>\d+) (?=green)",
    r"(?P<blue>\d+) (?=blue)",
    r"(?P<red>\d+) (?=red)",
])

class Turn(namedtuple('Turn', ['red', 'green', 'blue'])):
    @classmethod
    def from_string(cls, s):
        red = 0
        green = 0
        blue = 0
        for m in re.finditer(RE_TURN, s):
            match m.lastgroup:
                case 'red':
                    red = int(m.group('red'))
                case 'blue':
                    blue = int(m.group('blue'))
                case 'green':
                    green = int(m.group('green'))

        return cls(red=red, green=green, blue=blue)
    
    def possible(self, red, green, blue):
        return (self.red <= red and self.green <= green and self.blue <= blue)

class Game(namedtuple('Game', ['gid', 'turns'])):
    def possible(self, red, green, blue):
        return all([t.possible(red, green, blue) for t in self.turns])
    
    def min_cubes(self):
        red = max([t.red for t in self.turns])
        green = max([t.green for t in self.turns])
        blue = max([t.blue for t in self.turns])
        return (red, green, blue)
    
    def power(self):
        return F.reduce(int.__mul__, self.min_cubes())

def part1(buffer):
    r = 0
    for l in buffer:
        game_str, l = l.split(":", 1)
        gid = int(re.match(RE_GAME, game_str).group('id'))
        turns = [Turn.from_string(s) for s in l.split(';')]
        game = Game(gid, turns)
        if game.possible(12, 13, 14):
            r += game.gid
    return r

def part2(buffer):
    r = 0
    for l in buffer:
        game_str, l = l.split(":", 1)
        gid = int(re.match(RE_GAME, game_str).group('id'))
        turns = [Turn.from_string(s) for s in l.split(';')]
        game = Game(gid, turns)
        r += game.power()
    return r