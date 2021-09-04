#!/usr/bin/python

import util

max = 28123

if __name__ == "__main__":
    diabundants = [0]*(max+1)
    abundants = [i for i in range(1,max) if util.is_abundant(i)]
    for i in abundants:
        for j in abundants:
            if i+j <= max:
                diabundants[i+j] = 1
            else:
                # since list is sorted, we can quit early
                break
    print((sum(p[0] for p in enumerate(diabundants) if p[1] == 0)))
