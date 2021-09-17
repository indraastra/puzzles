from fractions import Fraction

def sqrt2(limit):
    prev = 1
    for i in range(limit):
        prev = 1 + Fraction(1, 1 + prev)
        yield prev


print(sum(len(str(frac.numerator)) > len(str(frac.denominator)) for frac in sqrt2(1000)))
