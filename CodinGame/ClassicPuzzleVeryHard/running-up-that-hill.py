from enum import IntEnum
import sys

def debug(*args):
    print(*args, file=sys.stderr, flush=True)

import numpy as np
import math as M
import itertools as I

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
        
class MatrixArithmetic:
    @classmethod
    def det(cls, m: np.matrix) -> int:
        return int(round(np.linalg.det(m)))

    @classmethod
    def cofactors(cls, m: np.matrix) -> np.matrix:
        cof = np.zeros_like(m)
        for (i, j), _ in np.ndenumerate(m):
            a = np.matrix(np.delete(np.delete(m, i, 0), j, 1))
            sgn = 1 if ((i+j) % 2 == 0) else -1
            cof[(i, j)] = sgn * cls.det(a)
        return cof

    @classmethod
    def adjugate(cls, m: np.matrix) -> np.matrix:
        return cls.cofactors(m).T
                
class MatrixModularArithmetic:
    def __init__(self, mod: int):
        self.mod = mod

    def multiplicative_inverse(self, a: int) -> int:
        g, x, y = egcd(a % self.mod, self.mod)
        if g != 1:
            raise ValueError(f"{a} has no multiplicative inverse modulo {self.mod}.")
        return x % self.mod

    def is_invertible(self, m: np.matrix) -> bool:
        det = MatrixArithmetic.det(m)
        g = M.gcd(det, self.mod)
        return g == 1

    def inverse(self, m: np.matrix) -> np.matrix:
        if not self.is_invertible(m):
            raise ValueError(f"matrix is not invertible modulo {self.mod}.")

        det = MatrixArithmetic.det(m)
        det_inv = self.multiplicative_inverse(det)
        adj = MatrixArithmetic.adjugate(m)
        return np.matrix((det_inv * adj) % self.mod)

class OCMLSS:
    def __init__(self, mod: int):
        self.mod = mod

    def solve(self, a, b):
        mma = MatrixModularArithmetic(self.mod)
        l = a.shape[0]
        s = a.shape[1]
        for idx in I.combinations(range(l), s):
            a0 = a[np.ix_(idx)]
            b0 = b[np.ix_(idx)]
            if mma.is_invertible(a0):
                a0_inv = mma.inverse(a0)
                k = np.matmul(a0_inv, b0).T % self.mod
                k_inv = mma.inverse(k)

                s0 = np.matmul(k, a.T) % self.mod
                s1 = b.T
                if np.equal(s0, s1).all():
                    return k, k_inv
                else:
                    continue
        raise ValueError("System is not solvable.")


LEXICON = IntEnum("Lexicon", [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z", " ", "$", "%", "*",
    "+", "-", ".", "/", ":"
])

def encode(p: str) -> np.array:
    p = np.array([LEXICON[s].value - 1 for s in p])
    return p

def group(m: List[int], n: int) -> np.array:
    mat = m.reshape((-1, n), order='C')
    return mat
 
def decode(p):
    return "".join(map(lambda i: LEXICON(i + 1).name, p.flatten('F')))

def encrypt(m: np.array, k: np.matrix, mod: int):
    return np.array(np.matmul(k, m.T) % mod)


def do_crack(plaintext, cipher, sizes, mod):
    solver = OCMLSS(mod)

    for s in range(2, 7):
        if all([x % s == 0 for x in sizes]):
            try:
                p_enc = group(encode(plaintext), s)
                c_enc = group(encode(cipher), s)
                k, k_inv = solver.solve(p_enc, c_enc)
                return k, k_inv
            except ValueError as e:
                debug(e, s)
                continue
        else:
            continue
    return None, None

def do_decipher(ciphertext, key, mod):
    n = key.shape[0]
    c_enc = group(encode(ciphertext), n)
    p_enc = encrypt(c_enc, key, mod)
    return decode(p_enc)
    
def do_cipher(plaintext, key, mod):
    n = key.shape[0]
    p_enc = group(encode(plaintext), n)
    c_enc = encrypt(p_enc, key, mod)
    return decode(c_enc)

cipher = input()
clear = input()
clear_me = input()
cipher_me = input()

sizes = len(cipher), len(clear), len(clear_me), len(cipher_me)
k, k_inv = do_crack(clear, cipher, sizes, 45)
p_me = do_decipher(clear_me, k_inv, 45)
c_me = do_cipher(cipher_me, k, 45)

print(p_me)
print(c_me)
