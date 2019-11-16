from util import is_subsequence
import psyco
import networkx as nx

def extremely_stupid_naive_brute_force_crap():
    """
    Generates all password strings from 4 to 7 digits and sees
    if any meet all the keylog requirements.

    Also fails. Utterly fails.
    """
    keystrokes = [l.strip() for l in open("keylog.txt")]
    for i in range(1000, 10000000):
        if i % 10000 == 0:
            print i
        password = str(i)
        if all(is_subsequence(password, keys) for keys in keystrokes):
            print password
            break

def read_key_edges(file):
    for l in open(file):
        l = l.strip()
        yield (l[0], l[1])
        yield (l[1], l[2])

def find_shortest_password(keylog):
    """
    Assumes each character occurs exactly once in password (big assumption). If
    this is true, the graph made from edges made from consecutive keylogged
    characters should be a DAG. If we topologically sort the resulting graph, a
    possible password should be the result.
    """
    edges = set(read_key_edges(keylog))
    G = nx.DiGraph()
    G.add_edges_from(edges)
    if nx.is_directed_acyclic_graph(G):
        print "graph is a DAG, topologically sorting"
        print "".join(nx.topological_sort(G))
    else:
        print "this algorithm cannot find a satisfactory solution for the input!"

if __name__ == "__main__":
    find_shortest_password("keylog.txt")
