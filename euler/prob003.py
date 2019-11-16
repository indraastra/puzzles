import math
import psyco

factors = []

i = 2
while i < math.sqrt ( 317584931803 ):
    if 317584931803 % i == 0:
        if len(factors) == 0:
            print i
            factors.append(i)
        else:
            bad = False
            for p in factors:
                if i % p == 0:
                    bad = True
                    break
            if not bad:
                print i
                factors.append(i)
    i += 1

print "done:", max(factors)
