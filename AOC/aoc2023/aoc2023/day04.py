from collections import namedtuple
import sys
import re

RE_CARD = r"^Card\s+\d+: (?P<winning>.*) \| (?P<numbers>.*)$"

Scratchcard = namedtuple('Scratchcard', ['winning', 'numbers'])
class Scratchcard(Scratchcard):
    @classmethod
    def from_string(cls, s):
        m = re.match(RE_CARD, s)
        winning = set(map(int, filter(bool, m['winning'].split(' '))))
        numbers = set(map(int, filter(bool, m['numbers'].split(' '))))
        return cls(winning=winning, numbers=numbers)
    
    def nmatch(self):
        return len(self.numbers.intersection(self.winning))
    def score(self):
        s = self.nmatch()
        if s > 0:
            return 2**(s-1)
        else:
            return 0


def part1(buffer):
    v = 0
    for l in buffer:
        l = l.strip()
        card = Scratchcard.from_string(l)
        v += card.score()
    return v

def part2(buffer):
    nmatch = []
    copies = []
    for l in buffer:
        l = l.strip()
        card = Scratchcard.from_string(l)
        nmatch.append(card.nmatch())
        copies.append(1)

    size = len(copies) - 1
    for i, n in enumerate(nmatch):
        c = copies[i]
        start = i + 1
        end = start + n
        for j in range(start, end):
            if j > size:
                break
            else:
                copies[j] += c
    return sum(copies)
