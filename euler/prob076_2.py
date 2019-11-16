#!/usr/bin/python
import psyco

from util import memoize

def num_partitions(n):
    total = 0
    for k in range(1, n/2):
        total += num_partitions_k(k, n-k)
    return total + 1

@memoize
def num_partitions_k(k, n):
    if k > n:
        return 0
    elif k == n:
        return 1
    else:
        return num_partitions_k(k+1, n) + num_partitions_k(k, n-k)

if __name__ == "__main__":
    for i in range(1,101):
        print i, "->", num_partitions(i)
