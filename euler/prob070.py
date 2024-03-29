import numpy as np
from tqdm import tqdm

import util

bound = 10**7

# Attempt 1 took ~18min on my laptop.
#primes = set(util.primes(bound))

def is_permutation(n1, n2):
  return sorted(str(n1)) == sorted(str(n2))

# def has_permuted_totient(n):
#  phi = util.totient(n, primes)
#  return is_permutation(n, phi)

# print(min((n for n in tqdm(range(2, bound)) if has_permuted_totient(n)),
#          key=lambda n: n / util.totient(n, primes)))

# Attempt 2 took ~1min.
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
  primes = set(i for i in range(2, limit) if len(
      factors[i]) == 1 and i in factors[i])
  return primes, factors


#primes, factors = primes_and_factors(bound)


def totient(n):
  if n in primes:
    return n - 1
  t = n
  for factor in factors[n]:
    t *= 1 - 1 / factor
  return int(round(t))


def has_permuted_totient(n):
  return is_permutation(n, totient(n))

# print(min((n for n in tqdm(range(bound-1, 5_000_000, -1)) if n not in primes and has_permuted_totient(n)),
#          key=lambda n: n / totient(n)))


# Attempt 3 takes 7s
# Like the prime sieve but for finding totient values:
def totients(limit):
  phis = np.arange(limit).astype(float)
  phis[:2] = 1
  phis[2::2] *= 1/2
  for i in tqdm(range(3, limit, 2)):
    if phis[i] == i:  # is prime
      phis[i::i] *= (1 - 1/i)
  return phis.astype(int)

# @np.vectorize
# def permutation_id(n):
#  return ''.join(sorted(str(n)))

# Technically this allows 88 == 880 == 880000, which allows more numbers to
# be equivalent than the sorted-string versions above. However, that's not an
# issue since we're still minimizing the value of n/phi(n) overall.


def permutation_id(arr, digits=8):
  powers_of_10 = 10 ** np.arange(digits)
  perms = (arr.reshape(-1, 1) // powers_of_10 % 10)
  perms.sort(axis=1)
  return (perms * powers_of_10[::-1]).sum(axis=1)


ns = np.arange(bound)
phis = totients(bound)
permutation_ids = permutation_id(ns)

# Option 1:
#is_prime = phis == ns-1
#bad_permutation = np.any(permutation_ids != permutation_ids[phis], axis=1)
#values = np.ma.masked_array(ns / phis, mask=is_prime|bad_permutation)
# print(values[2:].argmin()+2)

# Option 2:
not_prime = phis != ns-1
is_permutation = permutation_ids == permutation_ids[phis]
mask = not_prime & is_permutation
mask[:2] = False
print(ns[mask][(ns / phis)[mask].argmin()])
