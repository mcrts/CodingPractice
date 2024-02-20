from typing import Set
import numpy as np
from dataclasses import dataclass
import math
from pprint import pprint as pp
from enum import IntEnum
import sys


def debug(*args):
    print(*args, file=sys.stderr, flush=True)

@dataclass
class Modular:
    mod: int

    def extended_gcd(self, a: int, b: int):
        if (a == 0):
            x = 0
            y = 1
            return b, (x, y)
        
        gcd, (x1, y1) = self.extended_gcd(b % a, a)
        x, y = y1 - (b // a) * x1, x1
        return gcd, (x, y)


    def add(self, a: int, b: int) -> int:
        return (a + b) % self.mod
    
    def sub(self, a: int, b: int) -> int:
        return (a - b) % self.mod

    def mul(self, a: int, b: int) -> int:
        return (a * b) % self.mod
    
    def div(self, a: int, b: int) -> int:
        gcd = math.gcd(a, b) 
        if gcd != 1:
            a1 = a // gcd
            b1 = b // gcd
            try:
                q = (a1 * self.inv(b1)) % self.mod
            except ValueError as e:
                raise ValueError(f"{a1} is not divisible by {b1} modulo {self.mod}. Reduced from {a} / {b}") from e
        else:
            try:
                q = (a * self.inv(b)) % self.mod
            except ValueError as e:
                raise ValueError(f"{a} is not divisible by {b} modulo {self.mod}.") from e

        return q
    
    def is_coprime(self, a: int) -> bool:
        return math.gcd(self.mod, a) == 1
    
    def coprimes(self) -> Set[int]:
        return set(filter(self.is_coprime, range(self.mod)))
             
    def inv(self, a: int) -> int:
        if not self.is_coprime(a):
            raise ValueError(f"{a} is not a coprime of {self.mod}, {a} has not multiplicative inverse modulo {self.mod}.")
        
        _, (x, _) = self.extended_gcd(a, self.mod)
        return (x % self.mod + self.mod) % self.mod

@dataclass
class ModularMatrixAlgebra:
    mod: int

    def pivot(self, a, i):
        p = a[i, i]
        modulo = Modular(self.mod)
        vdiv = np.vectorize(lambda x: modulo.div(x, p))
        a[i] = vdiv(a[i])
        for j in range(a.shape[0]):
            if j != i:
                a[j] = modulo.add(a[j],  -1 * a[j, i] * a[i])
        return a
    
    def reduce(self, a, b):
        k = a.shape[0]
        m = np.hstack((a, b))
        debug(m)
        for i in range(k):
            m = self.pivot(m, i)

        return np.hsplit(m, k)[1]

    def inverse(self, a):
        i = np.eye(a.shape[0], dtype=int)
        return self.reduce(a, i)

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

def encrypt(p, key):
    return (np.matmul(key.T, p.T) % M).T

M = 45
mma = ModularMatrixAlgebra(M)

cipher = input()
clear = input()
clear_me = input()
cipher_me = input()

n = 2
p = encode(clear, n)
c = encode(cipher, n)
debug(clear)
debug(p)
debug(cipher)
debug(c)

k = mma.reduce(p[:n], c[:n])
debug(encrypt(p, k) == c)

print("cleared")
print("write ciphered")
