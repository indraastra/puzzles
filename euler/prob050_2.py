def sieve(limit):
 
    marked = [0] * limit
 
    marked[0] = marked[1] = 1
 
    for x in range(2, limit, 2):
        marked[x] = 1
 
    for x in range(3, limit, 2):
        if marked[x] == 0:
            for y in range(x*2, limit, x):
                marked[y] = 1
 
    return marked
 
primebits = sieve(1000000)
primes = []
primesums = []
 
for x in range(1000000):
    if primebits[x] == 0:
        primes.append(x)
 
limit = len(primes)//2
max = 0
 
for x in range(limit):
    sum = 0
    count = 0
    for y in range(x, limit):
        sum += primes[y]
        count += 1
        if sum > 999999: break
        if primebits[sum] == 0:
            primesums.append((sum, count))
            if count > max: max = count
    if limit - x < max: break
    #print x;
 
print('out')
 
for (x, y) in primesums:
    if y == max: print(x)
