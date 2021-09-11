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

if __name__ == "__main__":
    isPrime = [True]*1000001
    primes = []
    lens = [0]*1000001

    for i in range(2, 1000001):
        if isPrime[i]:
            primes.append(i)
            for j in range(i*i, 1000001, i):
                isPrime[j] = False

    limit = len(primes)
    maxlen = 0
    bestprime = 0
    for idx in range(limit):
        psum = 0
        for idx2 in range(idx, limit):
            p = primes[idx2]
            psum += p
            if psum >= 1000001:
                break
            elif isPrime[psum]:
                lensum = idx2-idx+1
                if lensum > maxlen:
                    bestprime = psum
                    maxlen = lensum
    print(bestprime, maxlen)


