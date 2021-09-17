from collections import defaultdict
import itertools
import util

limit = 1_000_000
primes = util.primes(limit)


def solve(count):
    for n in range(1, 4):
        patterns = defaultdict(set)
        for p in primes:
            s = str(p)
            idxs = defaultdict(set)
            for i, c in enumerate(s):
                idxs[c].add(i)
            for c, js in idxs.items():
                if len(js) < n: continue
                for idxs in itertools.combinations(js, n):
                    pattern = ''.join('*' if i in idxs else c
                                      for (i, c) in enumerate(s))
                    patterns[pattern].add(p)

        for pattern, ps in patterns.items():
            if len(ps) == count:
                return pattern, ps


if __name__ == '__main__':
    print(solve(8))
