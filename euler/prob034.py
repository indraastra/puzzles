import psyco
import util

for i in xrange(3, 10000000):
    if util.is_curious(i):
        print i
