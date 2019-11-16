#!/usr/bin/python

import psyco
import util

if __name__ == "__main__":
    amicable_numbers = set()
    for m in xrange(10000):
        n = sum(util.divisors_memoized(m))
        sum_d_n = sum(util.divisors_memoized(n))
        if sum_d_n == m and n != m:
            amicable_numbers.add(m)
    print sum(amicable_numbers)
