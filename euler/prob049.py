from collections import defaultdict
import itertools
import util

limit = 10_000
primutations = defaultdict(set)

for p in util.primes(limit):
    primutations[''.join(sorted(str(p)))].add(p)

for _, ps in primutations.items():
    if len(ps) < 3: continue
    for p1, p2, p3 in itertools.combinations(sorted(ps), 3):
        if p2 - p1 == p3 - p2:
            print(p1, p2, p3)

