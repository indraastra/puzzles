import functools

def trace(fn):
    @functools.wraps(fn)
    def _traced(*args, **kwargs):
        _traced.calls += 1
        print "%d: %s(*args=%s, **kwargs=%s)" % (_traced.calls, 
                                                 fn.__name__, 
                                                 args, kwargs)
        return fn(*args, **kwargs)
    _traced.calls = 0
    return _traced

def memoize(fn):
    cache = {}
    @functools.wraps(fn)
    def _memoized(*args):
        if args in cache:
            return cache[args]
        else:
            return cache.setdefault(args, fn(*args))
    return _memoized

# Debug test - change the order of these to witness the benefit of memoization.
@trace
@memoize
def levenshtein(s1, s2):
    if not (s1 and s2):
        return max(len(s1), len(s2))
    elif s1[0] == s2[0]:
        return levenshtein(s1[1:], s2[1:])
    else:
        return 1 + min((
            levenshtein(s1[1:], s2),
            levenshtein(s1, s2[1:]),
            levenshtein(s1[1:], s2[1:])
        ))
        
def main():
    a = "kitten"
    b = "mittens"
    c = levenshtein(a, b)
    print "distance between %s and %s is %s" % (a, b, c)
    
if __name__ == "__main__":
    main()