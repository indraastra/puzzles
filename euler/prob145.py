import psyco

def reverse_int(n):
    return int("".join(reversed(str(n))))

def odd(n):
    return (n % 2) == 1

def is_reversible(n):
    sum = n + reverse_int(n)
    return all(((int(i) % 2) == 0) for i in str(sum))

def solve_brute_force():
    """
    Takes too long, but was worth a shot.
    """
    max = 10**9
    count = 0
    for i in xrange(1, max, 2):
        if is_reversible(i):
            count += 1
    print count

def solve():
    pass

if __name__ == "__main__":
    solve_brute_force()
