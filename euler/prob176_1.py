import math

def squareComplements( n ):
    TC = 0
    c = 1
    n_sq = n ** 2
    while c * 2 + 1 < n_sq:
        tmp = math.sqrt( n_sq + c ** 2 )
        if  tmp % 1 == 0:
            if tmp > n:
                yield int(c)
        c += 1
        TC+=1
    print "TC:", TC

if __name__ == "__main__":
    i = 1000
    while True:
        print "checking:", i
        l = len( list( squareComplements( i ) ) )
        print "got:", l
        if l == 47547:
            print "found!:", i
            break
        else:
            i += 1
