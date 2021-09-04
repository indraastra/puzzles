# -*- coding: utf-8 -*-

import string

def permutations(xs):
    if len(xs) > 1:
        for i in range(len(xs)):
            xs_new = xs[:]
            x = xs_new.pop(i)
            xs_new = [x] + xs_new
            for p in permutations(xs_new[1:]):
                yield [xs_new[0]] + p
    else:
        yield xs

if __name__ == "__main__":
    i = 0
    for p in permutations(list(range(10))):
        i += 1
        if i == 1000000:
            print(''.join(map(str,p)))
            break
