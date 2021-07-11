from functools import reduce
# -*- coding: utf8 -*-
# n! means n × (n − 1) × ... × 3 × 2 × 1
# 
# Find the sum of the digits in the number 100!

def factorial(n):
    return reduce(lambda x,y: x*y, list(range(1,n+1)))

if __name__ == "__main__":
    print(factorial(100))
    print(sum(map(int,list(str(factorial(100))))))
