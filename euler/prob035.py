# -*- coding: utf8 -*-
# The number, 197, is called a circular prime because all rotations of the
# digits: 197, 971, and 719, are themselves prime.
# 
# There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71,
# 73, 79, and 97.
# 
# How many circular primes are there below one million?

import psyco
from util import rotations
 
def isCircular(p):
    for ns in rotations(map(int,list(str(p)))):
        n = int(''.join(map(str,ns)))
        if not isPrime[n]:
            return False
    return True


if __name__ == "__main__":
    isPrime = [True]*1000001
    primes = []

    for i in xrange(2, 1000001):
        if isPrime[i]:
            primes.append(i)
            for j in range(i*i, 1000001, i):
                isPrime[j] = False

    count = 0
    for p in primes:
        if p > 1000000:
            break
        if isCircular(p):
            print p
            count += 1
    print "count:", count
