import psyco
import math

class memoize:
    """
    from http://avinashv.net/2008/04/python-decorators-syntactic-sugar/
    """
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]

def choose(n, k):
    return factorial(n) / ( factorial(k) * factorial(n - k) )

_totients = {}
def totient(n, primes):
    if n in primes:
        return n - 1
    t = n
    factors = divisors_memoized(n)[1:]
    factors.append(n)
    for factor in factors:
        if factor in primes:
            t *= (1 - 1 / float(factor))
    return int(round(t))

def totient_memoized(n):
    if n in _totients:
        return _totients[n]
    else:
        _totients[n] = totient(n)
        return __totient[n]

digits = set([str(i) for i in range(1,10)])
def is_pandigital(m, n=9):
    s = str(m)
    if n != 9:
        _digits = set([str(i) for i in range(1, n + 1)])
    else:
        _digits = digits
    return len(s) == n and set(s) == _digits

def take(n, l):
    if isinstance(l, list):
        return l[:n]
    else:
        i = 0
        m = []
        for e in l:
            if i == n:
                break
            m.append(e)
            i += 1
        return m

def order(m, n):
    expt = 1
    prod = m
    while True:
        if prod % n == 1:
            return expt
        else:
            prod *= m
            expt += 1

def str2ints(string):
    return [ord(c) for c in string]

def ints2str(list, conv=chr):
    return ''.join(conv(i) for i in list)

def bin2dec(bitstring):
    """
    Converts a bitstring to decimal
    """
    return int(bitstring, 2)

def dec2bin(num):
    """
    Converts a decimal number to a bitstring
    """
    bits = []
    while num > 0:
        bits.append(str(num & 1))
        num = num >> 1
    bits.reverse()
    return ''.join(bits)

def prime_sieve(limit):
    is_prime = [1] * limit
    is_prime[0] = 0
    is_prime[1] = 0
    i = 3
    while i < limit:
        if i % 2 == 0:
            is_prime[i] = 0
        elif is_prime[i]:
            m = 2*i
            while m < limit:
                is_prime[m] = 0
                m += i
        i += 1
    return frozenset([i for i in xrange(limit) if is_prime[i]])

def primes(n): 
    """
    credit goes to someone else for this; it ended up being faster than my
    function above
    """
    if n==2: return [2]
    elif n<2: return []
    s=range(3,n+1,2)
    mroot = n ** 0.5
    half=(n+1)/2-1
    i=0
    m=3
    while m <= mroot:
        if s[i]:
            j=(m*m-3)/2
            s[j]=0
            while j<half:
                s[j]=0
                j+=m
        i=i+1
        m=2*i+3
    return [2]+[x for x in s if x]

def is_prime(n):
    factors = prime_factors(n)
    return factors == [n]

def is_palindrome(s):
    s = list(s)
    s_rev = s[:]
    s_rev.reverse()
    return s == s_rev

def combinations(l):
    pass

def permutations(l):
    if not l:
        yield []
    else:
        for n,i in enumerate(l):
            for p in permutations(l[:n]+l[n+1:]):
                yield [i]+p

def rotations(l):
    if not l:
        yield l
    else:
        for n in range(len(l)):
            yield l[n:]+l[:n]

_divisors = {}
def divisors(n):
    yield 1
    for i in xrange(2, int(math.sqrt(n))+1):
        if n % i == 0:
            yield i
            if i*i != n:
                yield n/i

def divisors_memoized(n):
    if n in _divisors:
        return _divisors[n]
    else:
        _divisors[n] = list(divisors(n))
        return _divisors[n]

@memoize
def prime_factors(n):
    i = 2
    while n > 1:
        if n % i == 0:
            return [i] + prime_factors(n/i)
        else:
            i += 1
    return []

_primes = (None, None)
def prime_factors_alt(n):
    global _primes
    if not _primes or _primes[0] < n:
        _primes = (n*2, primes(n*2))
    return _prime_factors_alt(n)

@memoize
def _prime_factors_alt(m):
    if m > 1:
        for p in _primes[1]:
            if m % p == 0:
                return [p] + _prime_factors_alt(m/p)
    else:
        return []

def is_abundant(n):
    return sum(divisors(n)) > n

def product(l):
    return reduce(lambda x: x*y, l)

_factorials = [1, 1, 2]
def factorial(n):
    if n <= len(_factorials) - 1:
        return _factorials[n]
    else:
        start = len(_factorials)
        for idx in xrange(start, n + 1):
            _factorials.append(idx * _factorials[idx - 1])
        return _factorials[-1]

def is_curious(n):
    return n == sum(factorial(int(c)) for c in str(n))

def int2list(n):
    return sorted([i for i in str(n)])

def normalize(d):
    total = float(sum(d.values()))
    for k in d:
        d[k] /= total
    return d

def is_subsequence(seq, sub):
    if len(sub) == 0:
        return True
    elif len(sub) > len(seq):
        return False
    elif len(sub) == len(seq):
        return sub == seq
    else:
        if seq[0] == sub[0]:
            rest = seq[1:]
            return is_subsequence(rest, sub) or is_subsequence(rest, sub[1:])
        else:
            return is_subsequence(seq[1:], sub)

def subsequences(sequence, n):
    if n == 0:
        yield []
    elif n == 1:
        for i in sequence:
            yield [i] 
    else:
        for i, el in enumerate(sequence):
            for subseq in subsequences(sequence[i:], n - 1):
                yield [el] + subseq
