#!/usr/bin/python
import psyco

print_tree = False
        
def num_ways_sum(n):
    return _num_ways_sum(n, n-1, 0)

def _num_ways_sum(n, max, indent):
    if n == 0:
        return 1
    total = 0
    for k in range(min(n, max), 0, -1):
        if print_tree:
            print "\t"*indent, "[",n,"]",k
        total += _num_ways_sum(n - k, max=k, indent=indent+1)
    return total

if __name__ == "__main__":
    prev = 0
    for i in range(1,51):
        curr = num_ways_sum(i)
        print i, "->", curr, "[", curr - prev, "]"
        prev = curr
