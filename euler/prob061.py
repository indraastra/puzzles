from collections import defaultdict
import itertools
import util


numbers = itertools.count


def triangle_number(n):
    return n*(n+1)//2


def square_number(n):
    return n**2


def pentagonal_number(n):
    return n*(3*n-1)//2


def hexagonal_number(n):
    return n*(2*n-1)


def heptagonal_number(n):
    return n*(5*n-3)//2


def octagonal_number(n):
    return n*(3*n-2)


def segues(a, b):
    p = len(a)//2
    return len(a) == len(b) and a[p:] == b[:p]


def is_cyclic(ns):
    return all(segues(a, b) for (a, b) in zip(ns, ns[1:]+[ns[0]]))


def summarize_targets(targets):
    for i, ts in enumerate(targets, 3):
        print(i, ':', len(ts))
    print('possibilities to check:', util.product(len(ts) for ts in targets))


fns = [triangle_number, square_number, pentagonal_number,
       hexagonal_number, heptagonal_number, octagonal_number]
target_len = 4
mid = target_len // 2


def prefix(s):
    return s[:mid]


def suffix(s):
    return s[mid:]


targets = [[] for _ in fns]
for n in numbers():
    under_target = False
    for i, f in enumerate(fns):
        f_n = str(f(n))
        if len(f_n) == target_len:
            targets[i].append(f_n)
        if len(f_n) <= target_len:
            under_target = True

    if not under_target:
        print(f'stopping at n={n}')
        summarize_targets(targets)
        break


edges = defaultdict(set)
nodes = set()
for deg, ns in enumerate(targets):
    for n in ns:
        node = (deg, n, suffix(n))
        nodes.add(node)
        edges[prefix(n)].add(node)


class Path:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.degrees = {n[0] for n in nodes}

    def __add__(self, node):
        return Path(self.nodes + [node])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str([n[:-1] for n in self.nodes])

    def current(self):
        return self.nodes[-1]

    def has_degree_of(self, node):
        return node[0] in self.degrees

    def is_cycle(self):
        return is_cyclic([n for (_, n, _) in self.nodes])

    def is_polygonal(self, target):
        return len(self.degrees) == target


def find_cycle(edges, nodes, target_deg):
    while nodes:
        to_visit = [Path([nodes.pop()])]
        while to_visit:
            path = to_visit.pop()
            if path.is_cycle() and path.is_polygonal(target_deg):
                return path

            # Visit this node.
            node = path.current()
            for child in edges[node[-1]]:
                if path.has_degree_of(child): continue
                to_visit.append(path + child)


cycle = find_cycle(edges, nodes, target_deg=len(fns))
if cycle is None:
    print('no solution found!')
else:
    print(cycle)
    print(sum(int(n[1]) for n in cycle.nodes))

# # Prune
# prefixes = [{prefix(t) for t in ts} for ts in targets]
# suffixes = [{suffix(t) for t in ts} for ts in targets]
# targets = [{t for t in ts
#             if (any(prefix(t) in ps for j, ps in enumerate(prefixes) if i != j) or
#                 any(suffix(t) in ss for k, ss in enumerate(suffixes) if i != k))}
#            for i, ts in enumerate(targets)]
# summarize_targets(targets)

# print(is_cyclic([str(d) for d in [8128, 2882, 8281]]))
