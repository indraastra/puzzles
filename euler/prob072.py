import psyco
import util

primes = util.prime_sieve(1000000)

sum = 0
for i in range(2, 1000001):
    sum += util.totient(i, primes)

print sum
