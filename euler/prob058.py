from fractions import Fraction
import itertools
import util

limit = 10_000_000
primes = set(util.primes(limit))

def is_prime(n):
    if n <= limit:
        return n in primes
    else:
        return util.is_prime(n)

def solve(frac):
    p_corners = 0
    c = 1
    for p in itertools.count(3, step=2):
        print(p)
        for _ in range(4):
            c += p - 1
            if is_prime(c):
                p_corners += 1
        #print(p_corners, 2 * p - 1, p)
        if p_corners / (2 * p - 1) < frac:
            return p_corners, p

print(solve(.1))
