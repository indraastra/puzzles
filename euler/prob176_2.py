import math
import psyco

def squareComplements( n ):
    TC = 0
    n_sq = n ** 2
    ### two cases:
    ### (n <= c < h) OR (c <= n < h)

    ### (n <= c < h)
    # c is at least n
    c = n
    # this condition ascertains that the nxn square contains enough "stuff" to
    # extend the cxc square's dimensions to an hxh square; c*2+1 is the minimum
    # amount of stuff that will be needed (it is exactly what is required to
    # extend the dimensions by 1 unit)
    while c * 2 + 1 < n_sq:
        tmp = math.sqrt( n_sq + c ** 2 )
        if  tmp % 1 == 0:
            yield int(c)
        TC+=1
        c += 1

    ### (c <= n < h)
    # cxc is at least the amount of stuff to extend the nxn square's dimensions
    # by 1 unit
    c = int( math.sqrt( n * 2 + 1 ) )
    while c < n:
        tmp = math.sqrt( n_sq + c ** 2 )
        if  tmp % 1 == 0:
            yield int(c)
        c += 1
        TC+=1
    #print "TC:",TC

if __name__ == "__main__":
    i = 3000
    while True:
        l = len( list( squareComplements( i ) ) )
        if l > 30:
            print i, "got:", l
        if l == 47547:
            print "found!:", i
            break
        else:
            i += 1
