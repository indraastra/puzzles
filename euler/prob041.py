import util
import itertools

def solve():
    """
    Generate permutations of range(1, n) and concatenate to form pandigital
    numbers. Start with n = 10 and count down until a prime pandigital is
    found.
    """
    for i in range(7, 1, -1):
        for p in itertools.permutations(list(range(i, 0, -1))):
            num = int("".join(str(i) for i in p))
            if (num % 2 != 0) and util.is_prime(num):
                print(num)
                return


if __name__ == "__main__":
    solve()
