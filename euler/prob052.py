import psyco
from util import int2list

min = -1
for i in range(6, 0, -1):
    for j in xrange(10**i+1, int((10**i)*1.7)):
        if int2list(j) == \
           int2list(2*j) == \
           int2list(3*j) == \
           int2list(4*j) == \
           int2list(5*j) == \
           int2list(6*j):
            min = j
print min
