#!/usr/bin/python

from __future__ import print_function
print(sum(n for n in range(1000) if (n % 3) == 0 or (n % 5) == 0))
