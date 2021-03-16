from tqdm import tqdm

import util

bound = 10**7

### Attempt 1 took ~18min on my laptop.
primes = set(util.primes(bound))

def is_permutation(n1, n2):
  return sorted(str(n1)) == sorted(str(n2))

#def has_permuted_totient(n):
#  phi = util.totient(n, primes)
#  return is_permutation(n, phi)

#print(min((n for n in tqdm(range(2, bound)) if has_permuted_totient(n)), 
#          key=lambda n: n / util.totient(n, primes)))
          
### Attempt 2 took ~1min.
# Like the prime sieve but for finding prime factors instead:
def primes_and_factors(limit):
  factors = [set() for i in tqdm(range(limit))]
  i = 2
  with tqdm(total=limit-i) as pbar:
    while i < limit:
      if i % 2 == 0:
        factors[i].add(2)
      elif not factors[i]:  # is prime 
        m = i
        while m < limit:
          factors[m].add(i)
          m += i 
      i += 1
      pbar.update(1) 
  primes = set(i for i in range(2, limit) if len(factors[i]) == 1)
  return primes, factors


primes, factors = primes_and_factors(bound)


def totient(n):
  if n in primes: return n - 1
  t = n
  for factor in factors[n]:
    t *= 1 - 1 / factor
  return int(round(t))

def has_permuted_totient(n):
  return is_permutation(n, totient(n))

print(min((n for n in tqdm(range(2, bound)) if n not in primes and has_permuted_totient(n)), 
          key=lambda n: n / totient(n)))

