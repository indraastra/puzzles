import psyco
from util import is_pandigital

arg = 0
max = 0
i = 1
while i <= 99999:
    n = 1
    digits = []
    while len(digits) < 9:
        digits.extend(list(str(i*n)))
        n += 1
    if len(digits) == 9 and is_pandigital(digits):
        num = int(''.join(digits))
        if num > max:
            max = num
            arg = i
    i += 1

print arg, max
