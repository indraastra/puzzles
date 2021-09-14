import util

primes = util.primes(9999)
primes_set = set(util.primes(99999999))

# pass 1: pairs
print("pairs")
conc_pairs = set()
for p1 in primes:
    for p2 in reversed(primes):
        if p1 < p2:
            p1str = str(p1)
            p2str = str(p2)
            if int(p1str+p2str) in primes_set and\
               int(p2str+p1str) in primes_set:
                   conc_pairs.add((p1,p2))
        else:
            break
print(conc_pairs)

# pass 2: triples
print("triples")
conc_triples = set()
for p1,p2 in conc_pairs:
    for p3 in reversed(primes):
        if p2 < p3:
            if (p1,p3) in conc_pairs and\
               (p2,p3) in conc_pairs:
                   conc_triples.add((p1,p2,p3))
        else:
            break

print(conc_triples)

# pass 3: quadruples
print("quads")
conc_quads = set()
for p1,p2,p3 in conc_triples:
    for p4 in reversed(primes):
        if p3 < p4:
            if (p1,p2,p4) in conc_triples and\
               (p1,p3,p4) in conc_triples and\
               (p2,p3,p4) in conc_triples:
                   conc_quads.add((p1,p2,p3,p4))
        else:
            break

print(conc_quads)

# pass 4: quintuples
print("quints")
conc_quints = set()
for p1,p2,p3,p4 in conc_quads:
    for p5 in reversed(primes):
        if p4 < p5:
            if (p1,p2,p3,p5) in conc_quads and\
               (p1,p2,p4,p5) in conc_quads and\
               (p1,p3,p4,p5) in conc_quads and\
               (p2,p3,p4,p5) in conc_quads:
                   conc_quints.add((p1,p2,p3,p4,p5))
        else:
            break

conc_quints = list(conc_quints)
conc_quints.sort(key=lambda x: sum(x))
print(conc_quints[0], sum(conc_quints[0]))
