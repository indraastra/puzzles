# -*- coding: utf-8 -*-

import psyco
import string

# create mappings from letters to scores
score_table = dict((x[1], x[0]+1) for x in enumerate(string.lowercase))
score_table.update(dict((x[1], x[0]+1) for x in enumerate(string.uppercase)))

def score(name, idx):
    return idx * sum(score_table[l] for l in name)

if __name__ == "__main__":
    f = open("names.txt")
    names = map(lambda x: x.strip(), f.readlines())
    names.sort()
    print sum(score(name, idx+1) for idx, name in enumerate(names))
