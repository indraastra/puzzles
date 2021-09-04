# -*- coding: utf8 -*-
# In England the currency is made up of pound, £, and pence, p, and there are
# eight coins in general circulation:
#    1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).
#
# It is possible to make £2 in the following way:
#    1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
#
# How many different ways can £2 be made using any number of coins?

def car(l):
    return l[0]

def cdr(l):
    return l[1:]

def numWays(amt, coins=[200,100,50,20,10,5,2,1]):
    if amt == 0:
        return 1
    elif len(coins) == 0:
        return 0
    elif car(coins) > amt:
        return numWays(amt, cdr(coins))
    else:
        return numWays(amt - car(coins), coins) + numWays(amt, cdr(coins))

if __name__ == "__main__":
    print(numWays(200))
