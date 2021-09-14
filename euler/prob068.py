
class Node:
    def __init__(self, id, gon):
        self.id = id
        self.gon = gon
        self.neighbors = set()
        self.reset()

    def set_value(self, v):
        self.value = v
        for n in self.neighbors:
            n.restrict(v)

    def add_neighbor(self, n):
        self.neighbors.add(n)

    def reset(self):
        self.possibilities = range(1, 11)
        self.value = 0

    def restrict(self, v):
        self.possibilities.remove(v)

    def __str__(self):
        return str(self.value)

class Link:
    def __init__(self, gon):
        self.gon = gon
        self.nodes = []

    def __str__(self):
        return ''.join(str(n) for n in self.nodes)

    def satisfied(self):
        return 9 == sum(n.value for n in self.nodes)

class Gon:
    def __init__(self, n):
        self.links = [Link(self) for i in range(n)]
        self.nodes = [Node(i, self) for i in range(2*n)]
        for i in range(n):
            if i == n-1:
                n1,n2,n3 = self.nodes[i], self.nodes[i+n], self.nodes[n]
            else:
                n1,n2,n3 = self.nodes[i], self.nodes[i+n], self.nodes[i+n+1]
            n1.add_neighbor(n2)
            n2.add_neighbor(n1)
            n2.add_neighbor(n3)
            n3.add_neighbor(n2)
            self.links[i].nodes = [n1, n2, n3]

    def __str__(self):
        strs = [str(l) for l in self.links]
        min_idx = min(enumerate(map(int,strs)), key=lambda x: x[1])[0]
        strs = strs[min_idx:] + strs[:min_idx]
        return ''.join(strs)

    def satisfied(self):
        for l in self.links:
            if not l.satisfied():
                return False
        all = range(1,11)
        vals = [n.value for n in self.nodes]
        vals.sort()
        return all == vals

if __name__ == "__main__":
    g = Gon(5)
    while not g.satisfied():

