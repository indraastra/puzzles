MAX = 200000

primes = [-1]*MAX
listofprimes = []

# 0 and 1 are not prime
primes[1] = 0
primes[0] = 0
# 2 is prime

i = 2
while i < MAX:
    if ( primes[i] != 0 ):
        primes[i] = 1
        listofprimes.append(i)
        #print "new prime:", i
        if len(listofprimes) == 10001:
            break
        j = 2*i
        while j < MAX:
            primes[j] = 0
            j += i
    else:
        primes[i] = 0
    i += 1

if len(listofprimes) == 10001:
    print("10001th prime:", listofprimes[10000])
else:
    print("set MAX higher")
