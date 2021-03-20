import util

import bisect
from fractions import Fraction
from tqdm import tqdm
import math
import numpy as np
import numpy.matlib

import functools
import time


def timer(func):
  # From https://realpython.com/python-timer/#a-python-timer-decorator
  @functools.wraps(func)
  def wrapper_timer(*args, **kwargs):
    tic = time.perf_counter()
    value = func(*args, **kwargs)
    toc = time.perf_counter()
    elapsed_time = toc - tic
    print(f"Elapsed time: {elapsed_time:0.4f} seconds")
    return value
  return wrapper_timer


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


@timer
def fractions_in_range(limit, lo, hi):
  fractions = set()
  for d in tqdm(range(2, limit+1)):
    for n in range(math.ceil(lo*d), math.ceil(hi*d)):
      f = Fraction(n, d)
      if lo < f < hi:
        fractions.add(f)
  return fractions


@timer
def fractions_in_range_vec(limit, lo, hi):
  total = 0
  for d in tqdm(range(2, limit+1)):
    v = np.arange(1, d+1) / d
    total += np.logical_and(v < hi, v > lo).sum()
  return total


@timer
def fractions_in_range_opt(limit, lo, hi):
  primes, factors = primes_and_factors(limit+1)
  total = 0
  for d in tqdm(range(2, limit+1)):
    lo_n = math.ceil(lo*d)
    hi_n = math.ceil(hi*d)
    if lo == Fraction(lo_n, d):
      lo_n += 1
    if d in primes:
      total += hi_n - lo_n
    else:
      total += sum(set.isdisjoint(factors[n], factors[d])
                   for n in range(lo_n, hi_n))
  return total


bound = 12_000
# Elapsed time: 96.4319 seconds
print(len(fractions_in_range(bound, Fraction(1, 3), Fraction(1, 2))))
# Elapsed time: 2.7290 seconds
print(fractions_in_range_opt(bound, Fraction(1, 3), Fraction(1, 2)))
