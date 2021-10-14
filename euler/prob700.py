import itertools
from math import ceil
import sys


def slow_eulercoins(euler, mod):
    last_coin = euler + 1
    current = euler
    skipped = 0
    while True:
        if current < last_coin:
            yield current
            last_coin = current
        else:
            skipped += 1
            print('skipping', current)

        if current == 0:
            print('bottomed out! skipped:', skipped)
            return

        current = (current + euler) % mod


def fast_eulercoins(euler, mod):
    sub   = mod % euler

    coins = []
    current = euler
    skipped = 0
    while True:
        if not coins or current < coins[-1]:
            yield current
            coins.append(current)
        else:
            skipped += 1
            #print('skipping', current)

        if current == 0:
            print('bottomed out! skipped:', skipped)
            return

        if current < sub:
            best = sub
            for c in reversed(coins[:-1]):
                next = (current + ceil((sub - current)/c)*c) % sub
                if next <= best:
                    best = next
                print('trying c', c, 'x', ceil((sub-current)/(c)), '->', next, current)
                if next <= current: break
            current = best % mod
            print('-> current', current)
        else:
            #current = (current - sub) % mod
            current = (current + euler) % mod


def fastest_eulercoins(euler, mod):
    delta = mod % euler
    odelta = delta
    coin = euler

    total = coin
    prev_coin = euler * 2

    yield coin
    print('found', coin, 'total', total, 'delta', delta)
    while coin > 1:
        if delta > coin:
            delta = delta % coin
        coin = coin - delta
        if coin < prev_coin:
            prev_coin = coin
            total += coin
            yield coin
            print('found', coin, 'total', total, 'delta', delta)


if __name__ == '__main__':
    #euler, mod = map(int, sys.argv[1:])
    #for eulercoins in [slow_eulercoins, fastest_eulercoins]:
    #    print(eulercoins)
    #    for i, e in enumerate(itertools.islice(eulercoins(euler, mod), 100)):
    #        print(f'{str(i).zfill(5)} >>>', e)
    #    print()
    euler = 1504170715041707
    mod   = 4503599627370517
    print(sum(fastest_eulercoins(euler, mod)))

