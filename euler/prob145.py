from collections import defaultdict

def reverse_int(n):
    return int(''.join(reversed(str(n))))

def odd(n):
    return (n % 2) == 1

def is_reversible(n):
    if n % 10 == 0:
        return False
    sum = n + reverse_int(n)
    return all(odd(int(i)) for i in str(sum))

def solve_brute_force(limit):
    """
    Takes too long, but was worth a shot.
    """
    count = 0
    count_by_len = defaultdict(int)
    found = []
    for i in range(1, limit, 2):
        if is_reversible(i):
            r = reverse_int(i)
            s = i + r
            #print(i, r, s)
            count_by_len[(len(str(i)), len(str(s)))] += 2
            found.append((s, i, r))
            count += 2
    print(count_by_len)
    #for s, i, r in sorted(found):
    #    print(s, i, r)
    return count

def solve():
    pass

if __name__ == "__main__":
    print(solve_brute_force(100_000_000))
