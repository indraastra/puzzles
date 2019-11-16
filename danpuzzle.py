ops = ['/','+','-','*']
# this function accepts a list of numbers and, by consuming expressions
# produced by the expression generator, egen(), produces a dictionary of
# expressions keyed by value as described below
def solve(l):
    # this dictionary is keyed by value into a list of expressions that
    # evaluate to that value
    d = {}
    # the map()s convert the input list of numbers into a list of strings
    # representing floats this counts as a list of expressions
    for exp in egen(map(str,map(float,l))):
        l = d.setdefault(eval(exp),[])
        l.append(exp)
    return d
# this function takes a list of expressions and generates (using "yield") ALL
# possible arithmetic expressions involving ALL of the expressions in the list
def egen(exps):
    if len(exps) == 1:
        yield exps[0]
    else:
        # generate all triples of the form <exp1,op,exp2>, but make sure we're
        # not duplicating expressions when we shouldn't be or dividing by 0.
        # and yes, i'm counting this as 2 lines
        triples = [(exps[i],op,exps[j]) for i in range(len(exps)) for j in range(len(exps)) for op in ops
                                        if (i != j) and not ((op == '/') and (eval(exps[j]) == 0))]
        for e1,op,e2 in triples:
            # remove used expressions from expression list and append newly
            # formed expression before recursing on resulting list
            exps.remove(e1)
            exps.remove(e2)
            newexp = '(' + e1 + op + e2 + ')'
            for e in egen(exps+[newexp]):
                yield e
            # add removed expressions back in
            exps.extend([e1,e2])
