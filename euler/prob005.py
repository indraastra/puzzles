import functools
import math

import util

n = functools.reduce(lambda x,y: x*y, util.primes(20), 1)
for i in range(2, 20):
  if n % i != 0:
    n *= i // math.gcd(i, n)
print(n)
