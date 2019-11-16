#!/usr/bin/python

import psyco
import util


def reduce_fraction(numerator, denominator):
    if denominator % numerator == 0:
        return (1, denominator / numerator)

if __name__ == "__main__":
    curious = []

    for d in range(10,100):
        for n in range(10,d):
            d1, d2 = map(int, tuple(str(d)))
            n1, n2 = map(int, tuple(str(n)))
            if n1 == d2:
                if n2/float(d1) == n/float(d):
                    curious.append((n, d))
            if n2 == d1:
                if d2 != 0:
                    if n1/float(d2) == n/float(d):
                        curious.append((n, d))

    print reduce_fraction(reduce(lambda x,y: x*y, [f[0] for f in curious]), 
                          reduce(lambda x,y: x*y, [f[1] for f in curious]))[1]
