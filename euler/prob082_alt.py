def read_matrix(file):
    return [[int(c) for c in l.rstrip().split(",")] for l in open(file)]

M = read_matrix("matrix.txt")
 
mtx = M 
size = len(mtx)
 
def get_column(n): return [mtx[i][n] for i in range(0,size)]
 
# start at the second last column
col = size - 2
current = get_column(col)
 
# the next column is the last one, so the minimum distance
# table is the last column, unchanged
next = get_column(size-1)
 
# now, the objective is to find the cheapest ways to get to
# next from current and save them as the new next, then go
# around again starting one column earlier
 
# calculate the route cost to go from current[x] to next[y]
# x and y count from 0
def route(x,y):
    cost = next[y]
    if x > y: return next[y] + sum(current[y:x+1])
    else: return next[y] + sum(current[x:y+1])
 
def cheapest():
    global next, col, current
    costs = []
    for x in range(0, size):
        costs.append(min([route(x,y) for y in range(0, size)]))
    col -= 1
    (next, current) = (costs, get_column(col))
 
while col >= 0: cheapest()
print min(next)
