from functools import lru_cache
from util import factorial


@lru_cache(maxsize=None)
def digital_factorial(n):
    return sum(factorial(int(d)) for d in str(n))


def chain_lengths(limit):
    chains = {}
    for s in range(limit):
        chain = []
        t = s
        while t not in chain:
            chain.append(t)
            t = digital_factorial(t)
            if t in chains:
                chains[s] = chains[t] + len(chain)
                break
        if s not in chains:
            pos = chain.index(t)
            cnt = len(chain)
            for i, u in enumerate(chain):
                # Progressively shorter chains until a ring.
                chains[u] = cnt - min(i, pos)
    return chains


if __name__ == '__main__':
    chains = chain_lengths(1_000_000)
    print(sum(kv[1] == 60 for kv in chains.items()))

