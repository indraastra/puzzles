import math
import psyco

def squareComplements( b ):
    # from http://en.wikipedia.org/wiki/Pythagorean_triple
    # method X
    odd = False
    if b % 2 != 0:
        odd = True
        mn = b
    else:
        mn = b / 2
    for fp in factorpairs( mn ):
        m, n = fp
        a = ( m ** 2 - n ** 2 )
        c = ( m ** 2 + n ** 2 )
        if odd:
            a, b = a/2, b/2
        yield ( a, b, c )

def factorpairs( n ):
    i = 1
    while i < math.sqrt( n ):
        if n % i == 0:
            yield ( n/i, i )
        i += 1

if __name__ == "__main__":
    i = 12
    l = list( squareComplements( i ) )
    print l
