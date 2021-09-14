
numNotBouncy = 0

def isNotBouncy(n):
    l = list(str(n))
    s = l[:]
    s.sort()
    r = s[:]
    r.reverse()
    return l != s and l != r

i = 1
while i < 10000000:
    if isNotBouncy(i):
        numNotBouncy += 1
    proportion = numNotBouncy/float(i)
    if proportion >= .99:
        print((i, proportion))
        break
    i += 1
