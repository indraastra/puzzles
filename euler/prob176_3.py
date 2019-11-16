import math
import psyco

def squareComplements( n ):
    stuff = n ** 2
    i = 1
    tc = 0
    extended_by = 0
    new_stuff = ( n * 2 * i ) + ( i ** 2 )
    c = math.sqrt( new_stuff )
    while ( new_stuff < stuff ):
        tc += 1
        if  c % 1 == 0:
            h = math.sqrt( new_stuff + stuff )
            extended_by = int( h - c )
            yield int( c )
        i += 1
        new_stuff = ( n * 2 * i ) + ( i ** 2 )
        c = math.sqrt( new_stuff )
    i = extended_by - 1
    new_stuff = stuff
    while ( i > 0 ):
        tc += 1
        c = ( new_stuff - i ** 2 ) / float ( 2 * i )
        stuff = c ** 2
        if  c % 1 == 0:
            yield int(c)
        i -= 1
    print tc

def factorpairs( n ):
    i = 2
    while i < math.sqrt( n ):
        if n % i == 0:
            yield ( i, n/i )
        i += 1

if __name__ == "__main__":
    i = 1000000
    while True:
        l = len( list( squareComplements( i ) ) )
        print i, "got:", l
        if l == 47547:
            print "found!:", i
            break
        else:
            i += 1
