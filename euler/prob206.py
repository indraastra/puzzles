import math
import re

endings = set()
for i in range(100, 10_000):
    s = str(i**2)
    if s[-1] == '0' and s[-3] == '9' and s[-5] == '8':
        endings.add(i % 1000)
print(endings)

lo = 1020304050607080900
hi = 1929394959697989990

sq_format = re.compile(r'^1\d2\d3\d4\d5\d6\d7\d8\d9\d0$')
def matches(s):
    return sq_format.match(s)

lo = math.floor(math.sqrt(lo))
lo = lo - (lo % 1000)
hi = round(math.sqrt(hi))
print(lo, hi)
for g in range(lo, hi+1, 1000):
    for e in endings:
        s = str((g+e)**2)
        if matches(s):
            print(g+e, s)
            break
