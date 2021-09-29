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


if __name__ == '__main__':
    euler, mod = map(int, sys.argv[1:])
    #euler = 1504170715041707
    #mod   = 4503599627370517

    print(euler, mod, mod % euler)
    for eulercoins in [slow_eulercoins, fast_eulercoins]:
    #for eulercoins in [fast_eulercoins]:
        print(eulercoins)
        for i, e in enumerate(itertools.islice(eulercoins(euler, mod), 100)):
            print(f'{str(i).zfill(5)} >>>', e)
        print()
