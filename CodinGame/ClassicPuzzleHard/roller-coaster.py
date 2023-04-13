import sys
from functools import cache

def debug(*args):
    print(*args, file=sys.stderr, flush=True)


"""
The program implement the following Graph Computation :
Given
    GROUPS a sequence of Integer [3, 1, 1, 2],
    L maximum size of a carriage,
    C the number of runs,
    I the cursor position,
When we start on I and execute C runs, what is the new value of I (Find where the cursor lands after C steps)
If we can solve this, it's easy to solve the real problem.

Initialization (I=0, C=8, L=3)
Solve(0, 8) -> I=3, S=19
    Solve(0, 4) -> I=1, S=10
        Solve(0, 2) -> I=3, S=5
            Solve(0, 1) -> I=1, S=3 
            Solve(1, 1) -> I=3, S=2 
        Solve(3, 2) -> I=1, S=5
            Solve(3, 1) -> I=0, S=2
            Solve(0, 1) -> I=1, S=3
    Solve(1, 4) -> I=3, S=9
        Solve(1, 2) -> I=0, S=4
            Solve(1, 1) -> I=3, S=2
            Solve(3, 1) -> I=0, S=2
        Solve(0, 2) -> I=3, S=5

This work if the number of runs C is a power of 2.
To solve for any number of runs,
we will perform a power of 2 decomposition and solve iteratively for each power of 2
merging the results and moving the cursor along the way.
"""

class Solution:
    """
    Store the result of a computation :
        the result(total),
        where we are in the queue(cursor).
    
    Supports addition between Solution, such as :
        lhs + rhs => Solution(
            total=lhs.total + rhs.total,
            cursor=rhs.cursor
        )
    """
    def __init__(self, total: int, cursor: int):
        self.total = total
        self.cursor = cursor
    
    def __add__(self, rhs):
        return Solution(
            total=self.total + rhs.total,
            cursor=rhs.cursor
        )

    def __repr__(self):
        return f"Solution<total={self.total}, cursor={self.cursor}>"

class CircularCursor:
    """A Circular Cursor implementation that wraps around a given size n."""
    def __init__(self, idx, n):
        self.idx=idx
        self.n=n
    
    def increment(self):
        self.idx = (self.idx + 1) % self.n

L, C, N = [int(i) for i in input().split()]
GROUPS = [int(input()) for _ in range(N)]

@cache
def sub_f(cursor: int) -> Solution:
    """
    Given a cursor position find the Solution for a single run.
    Make sure the CircularCursor doesn't move past the starting point (emptying the queue).
    """
    c = 0
    k = CircularCursor(cursor, N)
    i = 0
    while (i < N) and ((c + GROUPS[k.idx]) <= L):
        c += GROUPS[k.idx]
        i += 1
        k.increment()
    return Solution(c, k.idx)

@cache
def f(cursor: int, n: int) -> Solution:
    """
    Given a cursor position and a number of runs, find the Solution recursively
    by implementing the computation graph.
    """

    if n == 1:
        return sub_f(cursor)
    else:
        left = f(cursor, int(n / 2))
        right = f(left.cursor, int(n / 2))
        return left + right

def power_of_2_decomposition(n):
    """Decompose any number into an array of integers each being a powers of 2."""
    binary = map(int, bin(n)[2:][::-1])
    enumerated = enumerate(binary)
    filtered = filter(lambda v: v[1], enumerated)
    return [2**x for x, _ in filtered]

def solve() -> Solution:
    """
    Solve the problem.
    1. Initialize an empty Solution.
    2. Decompose the initial problem into a sequence of problems characterized by a power of 2.
    3. Iteratively solve each problem and accumulate the results.
    """
    s = Solution(0, 0)
    values = power_of_2_decomposition(C)
    for n in values:
        s = s + f(s.cursor, n)
    return s

solution = solve()

debug(f"{L=}, {C=}, {N=}, {GROUPS=}")
debug(f"{solution=}")

print(solution.total)
