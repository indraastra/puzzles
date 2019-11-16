#!/usr/bin/python

from __future__ import print_function
fiba = 0
fibb = 1
sum = 0

while fibb < 4000000:
    if fibb % 2 == 0:
        sum += fibb
    fiba, fibb = fibb, fiba+fibb

print(sum)
