# -*- coding: utf8 -*-
# In the card game poker, a hand consists of five cards and are ranked, from
# lowest to highest, in the following way:
#     * High Card: Highest value card.
#     * One Pair: Two cards of the same value.
#     * Two Pairs: Two different pairs.
#     * Three of a Kind: Three cards of the same value.
#     * Straight: All cards are consecutive values.
#     * Flush: All cards of the same suit.
#     * Full House: Three of a kind and a pair.
#     * Four of a Kind: Four cards of the same value.
#     * Straight Flush: All cards are consecutive values of same suit.
#     * Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.
# 
# The cards are valued in the order:
# 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.
# 
# If two players have the same ranked hands then the rank made up of the
# highest value wins; for example, a pair of eights beats a pair of fives (see
# example 1 below). But if two ranks tie, for example, both players have a pair
# of queens, then highest cards in each hand are compared (see example 4
# below); if the highest cards tie then the next highest cards are compared,
# and so on.
# 
# The file, poker.txt, contains one-thousand random hands dealt to two players.
# Each line of the file contains ten cards (separated by a single space): the
# first five are player one's cards and the last five are player two's cards.
# You can assume that all hands are valid (no invalid characters or repeated
# cards), each player's hand is in no specific order, and in each hand there is
# a clear winner.
# 
# How many hands does player one win?

import psyco
from collections import defaultdict

def royal(h):
    first = h[0][0]
    nums = [c[0] for c in h]
    r = range(14,9,-1)
    if nums == r:
        return first
    else:
        return 0

def flush(h):
    suit = h[0][1]
    for c in h:
        if c[1] != suit:
            return False
    return True

def straight(h):
    first = h[0][0]
    nums = [c[0] for c in h]
    r = range(first,first-5,-1)
    if nums == r:
        return first
    else:
        return 0

def fullHouse(h):
    if (h[0][0] == h[1][0] == h[2][0] and h[3][0] == h[4][0]):
        return (h[0][0],h[3][0])
    elif (h[0][0] == h[1][0] and h[2][0] == h[3][0] == h[4][0]):
        return (h[0][0],h[2][0])
    else:
        return ()

def twoPair(h):
    if (h[0][0] == h[1][0] and h[2][0] == h[3][0]):
        return (h[0][0],h[2][0])
    elif (h[0][0] == h[1][0] and h[3][0] == h[4][0]):
        return (h[0][0],h[3][0])
    elif (h[1][0] == h[2][0] and h[3][0] == h[4][0]):
        return (h[1][0],h[3][0])
    else:
        return ()

def mostSame(h):
    d = defaultdict(int)
    for c in h:
        d[c[0]] += 1
    v = d.items()
    v.sort(key=lambda x:-x[1])
    return v[0]

def bestHand(h):
    s = straight(h)
    f = flush(h)
    if s and f:
        if royal(h):
            return 9000+s
        else:
            return 8000+s
    same = mostSame(h)
    if same[1] == 4:
        return 7000+same[0]
    fh = fullHouse(h)
    if fh:
        return 6000+fh[0]*15+fh[1]
    elif f:
        return 5500
    elif s:
        return 5000+s
    elif same[1] == 3:
        return 4000+same[0]
    tp = twoPair(h)
    if tp:
        return 3000+tp[0]*15+tp[1]
    elif same[1] == 2:
        return 2000+same[0]
    else:
        return 1

def tieBreaker(h1,h2):
    for i in range(5):
        if h1[i][0] > h2[i][0]:
            return 1
        else:
            return -1
    return 0

def winner(h1, h2):
    b1,b2 = bestHand(h1),bestHand(h2)
    if b1 > b2:
        return (1,b1,b2)
    elif b2 > b1:
        return (-1,b1,b2)
    else:
        return (tieBreaker(h1, h2),b1,b2)

def cardValue(c):
    if c == 'A':
        return 14
    elif c == 'K':
        return 13
    elif c == 'Q':
        return 12
    elif c == 'J':
        return 11
    elif c == 'T':
        return 10
    else:
        return int(c)

def nextHand():
    fh = open("poker.txt")
    for line in fh:
        cards = line.strip().split()
        h1 = cards[:5]
        h1 = [(cardValue(c[0]),c[1]) for c in h1]
        h2 = cards[5:]
        h2 = [(cardValue(c[0]),c[1]) for c in h2]
        sortkey = lambda x: -x[0]
        h1.sort(key=sortkey)
        h2.sort(key=sortkey)
        yield (h1,h2)

if __name__ == "__main__":
    games = 0
    p1wins = 0
    for h1,h2 in nextHand():
        games += 1
        score = winner(h1,h2)
        if score[0] == 1:
            p1wins += 1
            print h1, ":", score[1], ">", h2, score[2]
        else:
            print h1, ":", score[1], "<", h2, ":", score[2]
    print p1wins
