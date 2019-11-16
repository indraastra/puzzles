import heapq
import itertools
import math

def begins_with(x, y):
    """
    >>> begins_with(984412321, 98)
    True
    >>> begins_with(111, 111)
    True
    >>> begins_with(111, 12)
    False
    """
    return str(x).startswith(str(y))


def p_naive(L, n):
    """
    >>> p_naive(12, 1)
    7
    >>> p_naive(12, 2)
    80
    """
    pow_2 = 1
    m = 0
    j = 0
    while True:
        if begins_with(pow_2, L):
            m += 1
        if m == n:
            return j
        j += 1
        pow_2 *= 2

        
def pow_increment(L):
    """
    Finds the smallest j such that 2**j starts with 100...
    with a 0 for each digit of L except the first.

    >>> pow_increment(1)
    0
    >>> pow_increment(12)
    10
    >>> pow_increment(123)
    196
    """
    zeros = len(str(L)) - 1
    return p_naive(10**zeros, 1)


def p_fast(L, n):
    """
    >>> p_fast(12, 1)
    7
    >>> p_fast(12, 2)
    80
    >>> p_fast(123, 45)
    12710
    """
    incr = pow_increment(L)
    pow_2 = 1
    m = 0
    prev_j = 0
    j = 0
    values_checked = 0
    while True:
        values_checked += 1
        if not begins_with(pow_2, L):
            j += 1
            pow_2 *= 2
            continue
        #print('{}, Diff: {}, Checked: {}'.format(j, j - prev_j, values_checked))
        m += 1
        if m == n:
            return j
        prev_j = j
        j += incr
        pow_2 *= 2 ** incr
        
        
class SmartGuesser:
    """
    >>> g = SmartGuesser()
    >>> list(itertools.islice(g, 3))
    [0, 1, 2]
    >>> next(g)
    3
    >>> g.good_guess()
    >>> next(g)
    4
    >>> next(g)
    5
    >>> next(g)
    6
    >>> next(g)
    7
    >>> g.good_guess()
    >>> next(g)
    11
    >>> g = SmartGuesser(start_guess=5, increments=[20, 10])
    >>> list(itertools.islice(g, 5))
    [5, 15, 25, 6, 7]
    """

    def __init__(self, start_guess=0, increments=()):
        self.current = start_guess
        self.previous = start_guess
        self.previous_good = None
        self.increment_by = 0
        self.smart_increments = set(increments)
        self._update_increment_stream(initial=0)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current != self.previous_good and self.increment_by == 1:
            # If we previously had a bad guess and we have no smart guesses left,
            # increment previous.
            self.previous = self.current
        self.increment_by = next(self.increment_stream)
        self.current = self.previous + self.increment_by
        return self.current
    
    def _update_increment_stream(self, initial=None, fallback=1, new_increment=1):
        if new_increment != 1:
            self.smart_increments.add(new_increment)
        self.increment_stream = itertools.chain(
            [initial] if initial is not None else [],
            sorted(self.smart_increments),
            itertools.cycle([fallback]))

    def good_guess(self):
        # Update the current guess!
        if self.previous_good:
            # If we had a good guess previously, update the known good increments.
            self._update_increment_stream(new_increment=self.current - self.previous_good)
        self.previous = self.current
        self.previous_good = self.current


def approx_pow_2(exp, places):
    """
    >>> approx_pow_2(80, 2)
    12
    >>> approx_pow_2(193060223, 3)
    123
    """
    def g():
        return math.ceil(exp / math.log2(10)) - places
    def f():
        return exp - g() / math.log10(2)
    return math.trunc(math.pow(2, f()))


def p_faster(L, n):
    """
    >>> p_faster(12, 1)
    7
    >>> p_faster(12, 2)
    80
    >>> p_faster(123, 45)
    12710
    """
    places = len(str(L))
    guesser = SmartGuesser(increments=[pow_increment(L)])
    m = 0
    values_checked = 0
    for guess in guesser:
        values_checked += 1
        # This version was too slow:
        #    pow_of_2 = 2 ** guess
        #    if not begins_with(pow_of_2, L):
        #        continue
        if approx_pow_2(guess, places) != L:
            continue
        guesser.good_guess()
        m += 1
        if m == n:
            return guess


def p_correct(L, n):
    """
    The "smart" incrementer is greedy and can miss valid solutions.
    
    >>> p_correct(12, 1)
    7
    >>> p_correct(12, 2)
    80
    >>> p_correct(123, 45)
    12710
    """
    places = len(str(L))
    guess = 0
    m = 0
    values_checked = 0
    while True:
        values_checked += 1
        if approx_pow_2(guess, places) == L:
            m += 1
            if m == n:
                return guess
        guess += 1

 
class SmarterGuesser:
    """
    >>> g = SmarterGuesser()
    >>> list(itertools.islice(g, 3))
    [0, 1, 2]
    >>> next(g)
    3
    >>> g.good_guess()
    >>> next(g)
    4
    >>> next(g)
    5
    >>> next(g)
    6
    >>> next(g)
    7
    >>> g.good_guess()
    >>> next(g)
    11
    >>> g = SmarterGuesser(start_guess=5, increments=[20, 10])
    >>> list(itertools.islice(g, 5))
    [5, 15, 25, 6, 7]
    """

    def __init__(self, start_guess=0, increments=()):
        self.next = [start_guess]
        self.previous = start_guess
        self.previous_good = None
        self.considering = start_guess
        self.smart_increments = set(increments)
        self._add_increments(self.smart_increments)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.next:
            # Step from our previous attempt if we're out of options.
            self.previous += 1
            heapq.heappush(self.next, self.previous)
        self.considering = heapq.heappop(self.next)
        return self.considering
        
    def _new_increment(self, new_increment):
        if new_increment > 1 and new_increment not in self.smart_increments:
            self.smart_increments.add(new_increment)
        for increment in sorted(self.smart_increments):
            next_value = self.considering + increment
            if next_value not in self.next:
                heapq.heappush(self.next, next_value)

    def _add_increments(self, new_increments):
        for increment in new_increments:
            self._new_increment(increment)

    def good_guess(self):
        # If we had a good guess previously, update the known good increments.
        if self.previous_good:
            self._new_increment(self.considering-self.previous_good)
        self.previous_good = self.previous
        self.previous = self.considering


def p_fastest_correct(L, n):
    """
    >>> p_fastest_correct(12, 1)
    7
    >>> p_fastest_correct(12, 2)
    80
    >>> p_fastest_correct(123, 45)
    12710
    >>> p_fastest_correct(122, 10)
    3289
    """
    places = len(str(L))
    guesser = SmarterGuesser(increments=[pow_increment(L)])
    found = 0
    checked = 0
    lo = math.log10(L)
    lo -= int(lo)
    hi = math.log10(L + 1)
    hi -= int(hi)
    c = math.log10(2)
    for guess in guesser:
        checked += 1
        dec = guess * c
        dec -= int(dec)
        if lo <= dec <= hi:
            found += 1
            guesser.good_guess()
            if found == n:
                return guess


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print('Solution: ', p_fastest(123, 678910))
