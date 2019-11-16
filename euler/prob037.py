import psyco
import util

primes = set(util.primes(1000000))

def left_right(p):
    s = str(p)
    for i in range(len(s)):
        yield int(s[i:])

def right_left(p):
    s = str(p)
    for i in range(1, len(s)+1):
        yield int(s[:i])


def all_prime(l):
    return all(p in primes for p in l)

if __name__ == "__main__":
    sum = 0
    num = 0
    for p in primes:
        if p not in [2,3,5,7]:
            if all_prime(left_right(p)) and all_prime(right_left(p)):
                sum += p
                num += 1
    print "found:", num
    print "sum:", sum
