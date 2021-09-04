# -*- coding: utf-8 -*-
import string

# create mappings from letters to scores
score_table = dict((x[1], x[0]+1) for x in enumerate(string.ascii_lowercase))
score_table.update(dict((x[1], x[0]+1) for x in enumerate(string.ascii_uppercase)))

def score(name, idx):
    return idx * sum(score_table[l] for l in name)

if __name__ == "__main__":
    f = open("names.txt")
    names = [x.strip() for x in f.readlines()]
    names.sort()
    print((sum(score(name, idx+1) for idx, name in enumerate(names))))
