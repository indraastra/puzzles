end = 1000
ndigits = 10
sum = 0

for i in range(1, end+1):
    print i, "^", i, "+"
    sum = (sum + (i ** i )) % 10 ** ndigits

print sum
