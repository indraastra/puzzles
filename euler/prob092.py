from functools import lru_cache

@lru_cache(maxsize=None)
def sq_char(c):
    return int(c)**2

def sum_sq_digits(n):
    return sum(map(sq_char, str(n)))

@lru_cache(maxsize=None)
def loops_to(n):
    if n == 1: return 1
    elif n == 89: return 89
    else: return loops_to(sum_sq_digits(n))


print(sum(loops_to(i) == 89 for i in range(1, 10_000_000)))
