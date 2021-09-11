
def num_digits(places):
    return 9*places*(10**(places-1))

def nth_digit(n):
    n = n - 1
    places = 1
    running = num_digits(places)
    while running < n:
        places += 1
        running += num_digits(places)
    running -= num_digits(places)
    reduced = n - running
    num = 10**(places-1) + reduced / places
    digit = reduced % places
    return int(str(num)[digit])


print(nth_digit(1) * nth_digit(10) * nth_digit(100) * nth_digit(1000) * nth_digit(10000) * nth_digit(100000) * nth_digit(1000000))
