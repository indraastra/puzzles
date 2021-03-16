from __future__ import print_function
import math

factors = []

i = 2
n = 600851475143
while i < math.sqrt ( n ):
    if n % i == 0:
        if len(factors) == 0:
            print(i)
            factors.append(i)
        else:
            bad = False
            for p in factors:
                if i % p == 0:
                    bad = True
                    break
            if not bad:
                print(i)
                factors.append(i)
    i += 1

print("done:", max(factors))
