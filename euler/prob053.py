# -*- coding: utf-8 -*-
"""
How many, not necessarily distinct, values of  ^(n)C_(r), for 1 ≤ n ≤ 100, are
greater than one-million?

               1              
             1   1           
           1   2   1          
         1   3   3   1        
       1   4   6   4   1      
"""

def pascal_triangle(nrows):
    """
    Generates rows of Pascal's triangle.
    """
    previous_row = None
    for i in range(nrows):
        if not previous_row:
            previous_row = [1]
        else:
            previous_row = [previous_row[i] + previous_row[i + 1] for i in range(len(previous_row))
                            if (i + 1) < len(previous_row)]
            previous_row.insert(0, 1)
            previous_row.append(1)
        yield i, previous_row

if __name__ == "__main__":
    n = 100
    count = 0
    pt = pascal_triangle(n + 1)
    for i, row in pt:
        for j, nCr in enumerate(row):
            if nCr > 1000000:
                count += 1
                #print i, "choose", j, ":", nCr
    print(count)
