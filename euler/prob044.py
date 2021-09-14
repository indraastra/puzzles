import itertools

def pentagonal_numbers(count):
    for n in range(1, count+1):
        yield n*(3*n-1)//2

ps = set(pentagonal_numbers(10_000))


def diff(ab):
    return abs(ab[0]-ab[1])


def sum_and_diff_pentagonal(ab):
    return sum(ab) in ps and diff(ab) in ps


ab = min(filter(sum_and_diff_pentagonal, itertools.combinations(ps, 2)), key=diff)
print(ab)
print('diff:', diff(ab))
