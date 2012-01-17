# Bitvectors Genealogy
# http://itasoftware.com/careers/work-at-ita/hiring-puzzles.html
#
# Works for the small puzzle so far, may be too slow for the large one.

import collections
import math
import sys

INF = float("inf")
P_MUTATION = 0.2

def read_bitvectors(file):
    return [l.strip() for l in open(file)]

def read_solution(file):
    parents = [int(l) for l in open(file) if l.strip()]
    return [(p, c) for (c, p) in enumerate(parents) if p != -1]
        
def mutations(bv1, bv2):
    size = len(bv1)
    same = sum(1 if bv1[i] == bv2[i] else 0 for i in xrange(size))
    return same, size - same
  
def p_mutations((same, diff)):
    return (P_MUTATION ** diff) * ((1 - P_MUTATION) ** (same))

def make_edges_complete(bvs):
    edges = []
    for i in xrange(len(bvs)):
        for j in xrange(i + 1, len(bvs)):
            weight = -math.log(p_mutations(mutations(bvs[i], bvs[j])))
            edges.append((i, j, weight))
    return edges

def make_adj_matrix(dim):
    matrix = []
    for i in xrange(dim):
        matrix.append([INF] * dim)
    return matrix
    
def mst_prim(vertices, edges):
    size = len(vertices)
    adj_matrix = make_adj_matrix(size)
    for v1, v2, weight in edges:
        adj_matrix[v1][v2] = weight
        adj_matrix[v2][v1] = weight
    v_new = set([0])
    e_new = []
    while True:
        min_weight = INF
        min_edge = None
        for v1 in v_new:
            for v2 in xrange(size):
                if v2 in v_new: continue
                weight = adj_matrix[v1][v2]
                if weight < min_weight:
                    min_weight = weight
                    min_edge = (v1, v2)
        v_new.add(min_edge[1])
        e_new.append(min_edge)
        if len(v_new) == size:
            break
    return e_new

def mst_compare(mst1, mst2):
    edges1 = set((min(v1, v2), max(v1, v2)) for (v1, v2) in mst1)
    edges2 = set((min(v1, v2), max(v1, v2)) for (v1, v2) in mst2)
    if edges1 != edges2:
        for p, c in edges1.difference(edges2):
            print "<", (p, c)
        for p, c in edges2.difference(edges1):
            print ">", (p, c)
    else:
        print "solution matched!"


# USELESS
def make_numeric(bv_str):
    return [int(c) for c in bv_str]

def signature(bv):
    return (bv.count("0"), bv.count("1"))
# /USELESS

def main():
    vertices = read_bitvectors(sys.argv[1])
    edges = make_edges_complete(vertices)
    mst = mst_prim(vertices, edges)
    solution_mst = read_solution(sys.argv[2])
    mst_compare(mst, solution_mst)

if __name__ == "__main__":
    main()
