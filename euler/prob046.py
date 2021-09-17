import bisect
import math
import util

limit = 1_000_000
primes = util.primes(limit)
primes_set = set(util.primes(limit))
deltas = set(2*i**2 for i in range(1, int(math.sqrt(limit))//4+1))

def primes_idx(n):
    return bisect.bisect_left(primes, n)


def is_square(n):
    return int(math.sqrt(n)**2) == n


def goldbach_holds(n):
    i = primes_idx(n)
    for p in primes[i-1:0:-1]:
        if (n - p) in deltas:
            return True


for n in range(33, limit, 2):
    if n in primes_set:
        continue
    # Odd composites beyond this point only.
    if not goldbach_holds(n):
        print(n)
        break
