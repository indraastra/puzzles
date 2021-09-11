# -*- coding: utf8 -*-
# The prime 41, can be written as the sum of six consecutive primes:
#   41 = 2 + 3 + 5 + 7 + 11 + 13
# 
# This is the longest sum of consecutive primes that adds to a prime below
# one-hundred.
# 
# The longest sum of consecutive primes below one-thousand that adds to a
# prime, contains 21 terms, and is equal to 953.
# 
# Which prime, below one-million, can be written as the sum of the most
# consecutive primes?

isPrime = [True]*1000001
primes = []

for i in range(2, 1000001):
    if isPrime[i]:
        primes.append(i)
        for j in range(i*i, 1000001, i):
            isPrime[j] = False

def primeSum(p):
    if isPrime[p]:
        idx = primes.index(p)
        sublists = [primes[a:b] for a in range(idx+1) for b in range(idx+1) if a < b if sum(primes[a:b]) == p]
        if len(sublists) == 0:
            return []
        longest = max(sublists, key=len)
        return longest
    else:
        return []

if __name__ == "__main__":
    bestSoFar = 0
    bestLength = 0
    for p in reversed(primes):
        print(p)
        l = primeSum(p)
        if len(l) > bestLength:
            bestSoFar = p
            bestLength = len(l)
    print(bestSoFar, bestLength)
