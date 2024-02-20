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
    
    def inverse(self, a):
        d = int(round(np.linalg.det(a))) % self.mod
        
        return self.reduce(a, i)
    
    def crack(self, plain, cipher):
        n_values = find_n(len(plain))
        n = None
        k0 = None
        k1 = None
        for n in n_values:
            try:
                p = encode(plain, n)
                c = encode(cipher, n)
                a = 1
                b = 2
                p = p[[a, b]]
                c = c[[a, b]]
                k0 = self.reduce(p, c)
                k1 = self.reduce(c.T, p.T)
                break
            except ValueError as e:
                debug(e)
                continue
        return n, k0, k1

M = 45
cipher = input()
clear = input()
clear_me = input()
cipher_me = input()

mma = ModularMatrixAlgebra(M)
n, k0, k1 = mma.crack(clear, cipher)
print(n)
print(k0)
print(k1)
sys.exit(0)

n, key, key_1 = crack(clear, cipher)
print(n)
print(key)
print(key_1)

cleared = decode(encrypt(encode(clear_me, n), key_1))
ciphered = decode(encrypt(encode(cipher_me, n), key))

print(cleared)
print(ciphered)