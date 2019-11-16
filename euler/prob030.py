# -*- coding: utf8 -*-
# Surprisingly there are only three numbers that can be written as the sum of
# fourth powers of their digits:
# 
#     1634 = 1^4 + 6^4 + 3^4 + 4^4
#     8208 = 8^4 + 2^4 + 0^4 + 8^4
#     9474 = 9^4 + 4^4 + 7^4 + 4^4
# 
# As 1 = 1^4 is not a sum it is not included.
# 
# The sum of these numbers is 1634 + 8208 + 9474 = 19316.
# 
# Find the sum of all the numbers that can be written as the sum of fifth
# powers of their digits.

import psyco

if __name__ == "__main__":
    e = 5
    total = 0
    i = 2
    while True:
        ns = map(int, list(str(i)))
        # if the best we can do with this many digits is not good enough, stop
        if len(ns)*(9**e) < i:
            print "stopping at", i
            break
        if i == sum(map(lambda x: x**e, ns)):
            print i
            total += i
        i += 1
    print "total", total
