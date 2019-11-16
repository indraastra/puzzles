import scipy
import psyco

def read_matrix(file):
    return [[int(c) for c in l.rstrip().split(",")] for l in open(file)]

def weighted_distance(col_a, i, col_b, j):
    if i > j:
        return col_b[j] + col_a[j:i+1].sum()
    else:
        return col_b[j] + col_a[i:j+1].sum()

if __name__ == "__main__":
    # initialize the number matrix
    M = scipy.array(read_matrix("matrix.txt"), int)

    # starting column is the last column
    dim_x, dim_y = M.shape
    col = dim_x - 1

    # initialize the cost array, which represents the least cost for going
    # from a particular cell in the current column to a cell in the next column
    C = M[:, col]

    # loop over columns backwards
    col -= 1
    while col >= 0:
        current = M[:, col]
        C = [min(weighted_distance(current, i, C, j) for j in range(dim_y)) for i in range(dim_x)]
        col -= 1
    print min(C)
