def solve(l):
    return egen(map(str,map(float,l)), {})
def egen(exps, d):
    if len(exps) == 1:
        d[eval(exps[0])].append(exps[0]) if eval(exps[0]) in d else d.setdefault(eval(exps[0]),[exps[0]])
    else:
        triples = [(i,op,j) for i in range(len(exps)) for j in range(len(exps)) for op in ["+","-","*","/"] if (i != j) and not ((op == '/') and (eval(exps[j]) == 0))]
        [egen([e for n,e in enumerate(exps) if i != n and j != n] + ['(' + exps[i] + op + exps[j] + ')'], d) for i,op,j in triples]
    return d
