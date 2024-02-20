from typing import Set
import numpy as np
from dataclasses import dataclass
import math
from pprint import pprint as pp
from enum import IntEnum
import sys
import itertools as it


def debug(*args):
    print(*args, file=sys.stderr, flush=True)

LEXICON = IntEnum("Lexicon", [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z", " ", "$", "%", "*",
    "+", "-", ".", "/", ":"
])

def encode(p, n):
    p = map(lambda s: LEXICON[s].value - 1, p)
    groups = np.array(list(zip(*(iter(p),) * n)))
    return groups

def decode(p):
    return "".join(map(lambda i: LEXICON(i + 1).name, p.flatten()))

def encrypt(p, key):
    return (np.matmul(key.T, p.T) % M).T

def _bruteforce(p, c, mod, n, i):
    values = it.product(*[list(range(mod)) for _ in range(n)])
    
    for k in values:
        key = np.array(k)
        if (encrypt(p, key) == c[:, i]).all():
            return key

def bruteforce(p, c, mod, n):
    return np.array([_bruteforce(p, c, mod, n, i) for i in range(n)]).T
        
def find_n(size):
    upper = math.floor(math.sqrt(size))
    lower = 2
    values = set()
    for n in range(lower, upper + 1):
        if size % n == 0:
            values.add(n)
    return values
        
def crack(plain, cipher):
    n_values = find_n(len(plain))
    for n in n_values:
        try:
            p = encode(plain, n)
            c = encode(cipher, n)
            k = bruteforce(p, c, M, n)
            k_1 = bruteforce(c, p, M, n)
        except ValueError as e:
            debug(e)
            continue
    return n, k, k_1

M = 45
cipher = input()
clear = input()
clear_me = input()
cipher_me = input()

n, key, key_1 = crack(clear, cipher)
print(n)
print(key)
print(key_1)

cleared = decode(encrypt(encode(clear_me, n), key_1))
ciphered = decode(encrypt(encode(cipher_me, n), key))

print(cleared)
print(ciphered)