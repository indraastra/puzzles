#!/usr/bin/python

import util

primes = util.prime_sieve(3000)

def consecutive_primes(a, b):
    num = 0
    x = 0
    while True:
        y = x ** 2 + a * x + b
        if y in primes:
            num += 1
        else:
            break
        x += 1
    return num

if __name__ == "__main__":
    max = 0
    max_coeffs = None
    for a in range(1000):
        for b in range(1000):
            if b not in primes:
                continue
            num = consecutive_primes( a, b)
            if num > max:
                max = num
                max_coeffs = (a,b)
            num = consecutive_primes(-a, b)
            if num > max:
                max = num
                max_coeffs = (-a,b)
            num = consecutive_primes( a,-b)
            if num > max:
                max = num
                max_coeffs = (a,-b)
            num = consecutive_primes(-a,-b)
            if num > max:
                max = num
                max_coeffs = (-a,-b)
    print((max, max_coeffs))
    print(("product:", max_coeffs[0] * max_coeffs[1]))

