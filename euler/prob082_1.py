import scipy
import psyco
import networkx as nx

def read_matrix(file):
    return [[int(c) for c in l.rstrip().split(",")] for l in open(file)]

def coord_to_index(y, x, dim_y):
    return x * dim_y + y

def edge_cost(G, i, j):
    return G.get((i, j), float("inf"))

def is_in_bounds(y, x, dim_y, dim_x):
    return 0 <= x < dim_x and 0 <= y < dim_y

def add_edge(G, e, w):
    G.add_edge(e[0], e[1], w)

def floyd_warshall(G, num_nodes):
    # initialize paths to edge costs
    print "initializing paths!"
    path = scipy.array([[edge_cost(G, i, j) for i in range(num_nodes)]for j in range(num_nodes)], float)

    print "computing shortest paths!"
    for k in range(num_nodes):
        print "done", k
        for i in range(num_nodes):
            for j in range(num_nodes):
                path[i][j] = min(path[i][j], path[i][k] + path[k][j])

if __name__ == "__main__":
    G = nx.DiGraph(weighted=True)
    M = scipy.array(read_matrix("matrix.txt"), int)
    dim_x, dim_y = M.shape
    # add normal edges
    for y in range(dim_y):
        for x in range(dim_x):
            node = coord_to_index(y, x, dim_y)
            next_nodes = [(y, x+1), (y+1, x), (y-1, x)]
            for y_next, x_next in next_nodes:
                if is_in_bounds(y_next, x_next, dim_y, dim_x):
                    next_node = coord_to_index(y_next, x_next, dim_y)
                    add_edge(G, (node, next_node), M[y][x])

    last_node = dim_x * dim_y - 1

    # add terminal nodes/edges
    for y in range(dim_y):
        node_y, node_x = y, dim_x - 1
        node = coord_to_index(node_y, node_x, dim_y)
        terminal_node = last_node + y + 1
        add_edge(G, (node, terminal_node), M[node_y][node_x])

    # run dijkstra's algorithm for all start node, end node pairs
    shortest_path_length = float("inf")
    for i in range(dim_y):
        print i
        for j in range(last_node + 1, last_node + dim_x + 1):
            shortest_path_length = min(shortest_path_length, nx.dijkstra_path_length(G, i, j))
    print shortest_path_length
