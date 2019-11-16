# dynamic programming!!!

# alternatively, just do (2n)!/(n!)^2

n = 20

# set up matrix
streets = [[0] * (n + 1) for i in range(n + 1)]
streets[n][n] = 1

def getnumpaths(i, j):
    if i > n:
        return 0
    elif j > n:
        return 0
    else:
        return streets[i][j]

for i in range(n, -1, -1):
    for j in range(i, -1, -1):
        if i == n and j == n:
            continue
        streets[i][j] = getnumpaths(i + 1, j) + getnumpaths(i, j + 1)
        streets[j][i] = getnumpaths(j + 1, i) + getnumpaths(j, i + 1)

for i in range(0, n+1):
    for j in range(0, n+1):
        print getnumpaths(i, j), ' ',
    print

#print streets[0][0]

