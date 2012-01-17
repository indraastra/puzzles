BitVector Genealogy

Observations
============

1. The problem is essentially one of finding the most likely BitVector family
tree given a set of BitVector organisms.

2. A genealogy of this sort can be represented as a rooted tree.

3. The probability one BitVector was cloned to another BitVector is (p_mut ^
n_mut) * (p_same ^ n_same).

4. This probability is symmetric.

5. The probability of an ancestry tree is the product of all individial
parent-offspring relationships.

6. Interestingly, it follows from the previous that given a rooted tree, any
node can be the root and the probability of the tree will remain unchanged.

7. It seems that given 6, there is no unique solution if the solution is
encoded as ITA does it, which is to say a rooted directed graph.

8. To compare solutions effectively, one must convert the graph to a tree and
check to see that the structures are isomorphic; only then do they represent
the same family tree.

9. Given a graph where nodes are BitVectors, a possible solution to find the
most likely family tree is to connect all nodes (make a complete graph) where
edge weights are probabilities. The best tree is the one with the highest
product of edge weights. If we take the negative log() of each edge, the
minimum spanning tree is effectively the best tree. To find this, we can use an
MST algorithm like Prim's or Kruskal's.

10. This approach has V^2 complexity in space and time, since it requires a
complete graph.

11. There may be some tricks to reduce the connectedness of the graph, but only
tricks that preclude generating ALL possible edges would make any sense, since
generating V^2 edges will be more expensive than finding the MST of a less
connected graph.

12. The expected number of mutations with a 20% chance and a 500-bit genome is
100. One could use some type of locality hashing to only form edges with LIKELY
clones rather than ALL organisms.

13. Or, one could just write this in C and hope that V^2 where V = 10000 isn't
so bad.
