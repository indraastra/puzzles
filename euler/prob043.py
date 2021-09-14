import itertools

total = 0
for digits in itertools.permutations(range(10)):
    if digits[3] % 2 != 0: continue
    if digits[5] not in (0, 5): continue
    n = ''.join(map(str, digits))
    if int(n[1:4]) % 2 != 0: continue
    if int(n[2:5]) % 3 != 0: continue
    if int(n[3:6]) % 5 != 0: continue
    if int(n[4:7]) % 7 != 0: continue
    if int(n[5:8]) % 11 != 0: continue
    if int(n[6:9]) % 13 != 0: continue
    if int(n[7:10]) % 17 != 0: continue
    total += int(n)
print(total)
