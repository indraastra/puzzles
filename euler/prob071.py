from fractions import Fraction
import math

winner = Fraction(2, 5)
target = Fraction(3, 7)

for d in range(8, 1_000_000):
    lo = math.ceil(winner * d)
    hi = math.ceil(target * d)
    for n in range(lo, hi):
        f = Fraction(n, d)
        if winner < f < target:
            winner = f
print(winner)
