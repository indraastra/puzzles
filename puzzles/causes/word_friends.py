from collections import deque
import functools
import string

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

# probably won't work so well with generators
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
            levenshtein(s1[1:], s2),     # delete from left
            levenshtein(s1, s2[1:]),     # delete from right
            levenshtein(s1[1:], s2[1:])  # admit mismatch
        ))
        
def test_levenshtein():
    a = "kitten"
    b = "mittens"
    c = levenshtein(a, b)
    print "distance between %s and %s is %s" % (a, b, c)


LEXICON = set(w.strip() for w in open("word.list"))

@memoize
def neighbors(word):
    words = []
    for i in xrange(len(word)):
        for c in string.lowercase:
            if c != word[i]:
                n_word = word[:i] + c + word[i+1:]
                if n_word in LEXICON: words.append(n_word)
            n_word = word[:i] + c + word[i:]
            if n_word in LEXICON: words.append(n_word)
        n_word = word[:i] + word[i:]
        if n_word in LEXICON: words.append(n_word)
    for c in string.lowercase:
        n_word = word + c
        if n_word in LEXICON: words.append(n_word)
    return words

@memoize
def neighbors_v2(word):
    words = set()
    # prefix letter to word
    for c in string.lowercase:
        words.add( c + word )
    # change first letter
    if len(word) >= 1:
        for c in string.lowercase:
            if c != word[0]:
                words.add( c + word[1:] )
        # recursively change something after first letter
        for n_word in neighbors_v2(word[1:]):
            words.add( word[0] + n_word )
        # postfix letter to word
        for c in string.lowercase:
            words.add( word + c )
    return words

def word_friends(word):
    friends = deque(neighbors(word))
    visited = set([word])
    while friends:
        friend = friends.popleft()
        visited.add(friend)
        for n_friend in neighbors(friend):
            if n_friend not in visited:
                friends.append(n_friend)
    return visited

def word_friends_v2(word):
    friends = deque([word])
    visited = set([word])
    while friends:
        friend = friends.popleft()
        visited.add(friend)
        for n_friend in neighbors_v2(friend):
            if n_friend in LEXICON and n_friend not in visited:
                friends.append(n_friend)
    return visited

if __name__ == "__main__":
    friends = list(word_friends("causes"))
    friends.sort()
    for word in friends:
        print word
    print len(friends), "friends found"
