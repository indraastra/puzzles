import util

def solve():
    """
    The n/phi(n) will be large when phi(n) is small and n is large. To make
    phi(n) small, we have to make n have as many divisors as possible. A good
    way to do this is to include small primes as some of its divisors.
    Multiples of these small primes will be ruled out from the totient, which
    is a good thing.  Not guaranteed to be the right answer, I suppose, but
    turns out to be.
    """
    primes = util.primes(1000000)
    product = 1
    phi = 0
    for p in primes:
        if product * p <= 1000000:
            print "multiplying one more prime:", p
            product *= p
            phi += 1
        else:
            break
    print "final n:", product
    print "phi(n):", phi
    print "n/phi(n):", product/float(phi)

if __name__ == "__main__":
    solve()

