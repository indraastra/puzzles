_digits = set(map(str, range(1, 10)))

def is_pandigital(m, n=9):
    return len(m) == n and set(m) == _digits

arg = 0
max = 0
i = 1
while i <= 99999:
    n = 1
    digits = []
    while len(digits) < 9:
        digits.extend(str(i*n))
        n += 1
    if is_pandigital(digits):
        num = int(''.join(digits))
        if num > max:
            max = num
            arg = i
    i += 1

print(arg, max)
