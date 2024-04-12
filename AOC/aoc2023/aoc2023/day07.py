from collections import namedtuple, Counter
import sys
import re

import itertools as I
import functools as F

from enum import Enum,IntEnum

class Card(IntEnum):
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    T = 9
    J = 10
    Q = 11
    K = 12
    A = 13

    @classmethod
    def from_char(cls, c):
        match c:
            case "2":
                return cls.TWO
            case "3":
                return cls.THREE
            case "4":
                return cls.FOUR
            case "5":
                return cls.FIVE
            case "6":
                return cls.SIX
            case "7":
                return cls.SEVEN
            case "8":
                return cls.EIGHT
            case "9":
                return cls.NINE
            case "T":
                return cls.T
            case "J":
                return cls.J
            case "Q":
                return cls.Q
            case "K":
                return cls.K
            case "A":
                return cls.A
        
class HandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

Hand = namedtuple("Hand", ["cards", "bet"])
class Hand(Hand):
    def value(self):
        d = Counter(self.cards)
        if 5 in d.values():
            v = HandType.FIVE_OF_A_KIND
        elif 4 in d.values():
            v = HandType.FOUR_OF_A_KIND
        elif 3 in d.values() and 2 in d.values():
            v = HandType.FULL_HOUSE
        elif 3 in d.values():
            v = HandType.THREE_OF_A_KIND
        elif len([x for x in d.values() if x == 2]) == 2:
            v = HandType.TWO_PAIR
        elif 2 in d.values():
            v = HandType.ONE_PAIR
        else:
            v = HandType.HIGH_CARD
        return (v, self.cards)
            
def part1(buffer):
    hands = []
    for l in buffer:
        l_cards, bet = l.strip().split(" ", 2)
        cards = [Card.from_char(c) for c in l_cards]
        hands.append(Hand(cards, int(bet)))
    ranked = sorted(hands, key=Hand.value)
    score = sum([(r+1) * h.bet for r, h in enumerate(ranked)])
    return score

class Card2(IntEnum):
    J = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    T = 9
    Q = 10
    K = 11
    A = 12

    @classmethod
    def from_char(cls, c):
        match c:
            case "2":
                return cls.TWO
            case "3":
                return cls.THREE
            case "4":
                return cls.FOUR
            case "5":
                return cls.FIVE
            case "6":
                return cls.SIX
            case "7":
                return cls.SEVEN
            case "8":
                return cls.EIGHT
            case "9":
                return cls.NINE
            case "T":
                return cls.T
            case "J":
                return cls.J
            case "Q":
                return cls.Q
            case "K":
                return cls.K
            case "A":
                return cls.A
            
Hand2 = namedtuple("Hand2", ["cards", "bet"])
class Hand2(Hand2):
    def full_house(self, counter):
        return (3 in counter.values() and 2 in counter.values())
    
    def base_value(self):
        d = Counter(filter(lambda c: c != Card2.J, self.cards))
        if 5 in d.values():
            v = HandType.FIVE_OF_A_KIND
        elif 4 in d.values():
            v = HandType.FOUR_OF_A_KIND
        elif 3 in d.values() and 2 in d.values():
            v = HandType.FULL_HOUSE
        elif 3 in d.values():
            v = HandType.THREE_OF_A_KIND
        elif len([x for x in d.values() if x == 2]) == 2:
            v = HandType.TWO_PAIR
        elif 2 in d.values():
            v = HandType.ONE_PAIR
        else:
            v = HandType.HIGH_CARD
        return (v, self.cards)
            
    def value(self):
        d = Counter(self.cards)
        n = d[Card2.J]
        base_value = self.base_value()

        match base_value[0], n:
            case (_, 0):
                v = base_value[0]
            case (HandType.FOUR_OF_A_KIND, 1):
                v = HandType.FIVE_OF_A_KIND
            case (HandType.THREE_OF_A_KIND, 1):
                v = HandType.FOUR_OF_A_KIND
            case (HandType.THREE_OF_A_KIND, 2):
                v = HandType.FIVE_OF_A_KIND
            case (HandType.TWO_PAIR, 1):
                v = HandType.FULL_HOUSE
            case (HandType.ONE_PAIR, 1):
                v = HandType.THREE_OF_A_KIND
            case (HandType.ONE_PAIR, 2):
                v = HandType.FOUR_OF_A_KIND
            case (HandType.ONE_PAIR, 3):
                v = HandType.FIVE_OF_A_KIND
            case (HandType.HIGH_CARD, 1):
                v = HandType.ONE_PAIR
            case (HandType.HIGH_CARD, 2):
                v = HandType.THREE_OF_A_KIND
            case (HandType.HIGH_CARD, 3):
                v = HandType.FOUR_OF_A_KIND
            case (HandType.HIGH_CARD, 4):
                v = HandType.FIVE_OF_A_KIND
            case (HandType.HIGH_CARD, 5):
                v = HandType.FIVE_OF_A_KIND
            case _:
                print("ERROR |", base_value[0], n)
        return (v, self.cards)


def part2(buffer):
    hands = []
    for l in buffer:
        l_cards, bet = l.strip().split(" ", 2)
        cards = [Card2.from_char(c) for c in l_cards]
        hands.append(Hand2(cards, int(bet)))
    ranked = sorted(hands, key=Hand2.value)
    score = sum([(r+1) * h.bet for r, h in enumerate(ranked)])
    return score