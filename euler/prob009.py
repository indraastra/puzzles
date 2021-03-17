import math

MAX = 998

for a in range ( 1, MAX ):
    for b in range ( a, MAX ):
        sumsquare = a ** 2 + b ** 2
        c = math.sqrt ( sumsquare )
        if c % 1 == 0:
            c = int ( c )
            if c + a + b == 1000:
                print("found!:", a, b, int ( c ))
                print("product is:", a*b*int ( c ))


