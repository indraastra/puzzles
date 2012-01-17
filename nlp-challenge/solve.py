import collections
import itertools
import math
import string

from nltk.corpus import gutenberg

LOWER = string.ascii_lowercase
ALL = LOWER + string.ascii_uppercase

################################################################################
# Helper functions.
################################################################################
def ascii_rotn(s, n):
  rot_lower = LOWER[n:] + LOWER[:n]
  trans = string.maketrans(ALL, rot_lower + rot_lower.upper())
  return string.translate(s, trans, string.punctuation)

def product(nums):
  """
  Returns the product of a sequence of numbers.
  """
  p = 1
  for n in nums:
    p *= n
  return p

def memoize(fn):
  cache = {}
  def wrapped(*args):
    if args in cache:
      return cache[args]
    else:
      return cache.setdefault(args, fn(args))

def ngrams(seq, n):
  end = len(seq) - n + 1
  for i in range(end):
    yield seq[i:i+n]

def slice(lines):
  slice_width = len(lines[0][0])
  num_slices = max(len(l) for l in lines)
  slices = []
  for i in range(num_slices):
    slices.append([lines[j][i] if i < len(lines[j]) else ' ' * slice_width
                  for j in range(len(lines))])
  return slices

def linearize(slices):
  lines = []
  num_lines = max(len(s) for s in slices)
  for i in range(num_lines):
    lines.append([slices[j][i] for j in range(len(slices))])
  return lines

def serialize(slices):
  return "".join("".join(l) for l in linearize(slices))

################################################################################
# Brute force approach.
################################################################################
def solve_p1_brute(file):
  text = open(file).read().strip()
  for i in range(26):
    rot_text = ascii_rotn(text, i)
    print i, rot_text


################################################################################
# Probabilistic approach.
################################################################################
class DictCorpus:
  def __init__(self, dict_file):
    self.total = 0
    self.words = collections.defaultdict(int)
    for l in open(dict_file):
      self.update(w.lower() for w in l.split())

  def update(self, words):
    for w in words:
      self.words[w] += 1
      self.total += 1

  def P_elem(self, word):
    # With very basic "smoothing"...
    return (self.words[word] + 1.0) / (self.total + 1.0)

  def W_elem(self, word):
    # With very basic "smoothing"...
    return (self.words[word] + 1.0)

  def P_sequence(self, sequence):
    """
    Returns the probability of a sequence of elements independently sampled 
    from a corpus.
    """
    return product(self.P_elem(elem) for elem in sequence)

  def W_seq(self, sequence):
    """
    Returns the weight of a sequence of elements independently sampled 
    from a corpus.
    """
    return product(self.W_elem(elem) for elem in sequence)

def solve_p1_prob(file):
  text = open(file).read().strip().lower()
  corpus = DictCorpus("/usr/share/dict/words")
  rot_texts = [ ascii_rotn(text, i).split() for i in range(26) ]
  # Unless we use relative weights, the probability pretty much zeroes out and
  # returns an arbitrary answer.
  print " ".join(max(rot_texts, key=corpus.W_seq))


class NgramLetterCorpus:
  def __init__(self, n):
    self.n = n
    self.counts = collections.defaultdict(int)

  def update(self, text):
    text = text.strip().lower()
    for ngram in ngrams(text, self.n):
      self.counts[ngram] += 1

  def W_elem(self, ngram):
    # With very basic "smoothing"...
    return math.log(self.counts[ngram] + 1.0)

  def W_seq(self, text):
    return sum(self.W_elem(ngram) for ngram in ngrams(text, self.n))

def insert(slices, src, dst):
  if src > dst:
    return slices[:dst] + [slices[src]] + slices[dst:src] + slices[src+1:]
  elif dst > src:
    return slices[:src] + slices[src+1:dst+1] + [slices[src]] + slices[dst+1:]
  else:
    return slices

def make_insert(slices, i, j):
  return (lambda slices: insert(slices, i, j),
          lambda slices: insert(slices, j, i))

def swap(slices, i, j):
  tmp = slices[i]
  slices[i] = slices[j]
  slices[j] = tmp
  return slices

def make_swap(slices, i, j):
  return (lambda slices: swap(slices, i, j),
          lambda slices: swap(slices, i, j))

def rotate(slices, n):
  return slices[n:] + slices[:n]

def make_rotate(slices, n):
  return (lambda slices: rotate(slices, n),
          lambda slices: rotate(slices, len(slices) - n))

def make_moves(slices):
  # sigh, if only closures worked properly, I could use lambdas here...
  insertions = [make_insert(slices, i, j)
                for (i, j) in itertools.permutations(range(len(slices)), 2)]
  swaps = [make_swap(slices, i, j)
           for (i, j) in itertools.combinations(range(len(slices)), 2)]
  #rotations = [make_rotate(slices, n)
  #             for n in range(1, len(slices))]
  return itertools.chain(insertions, swaps)

def evaluate1(slices, corpus):
  # evaluates in a rotation-invariant way...wtf?
  return max(corpus.W_seq(serialize(rotate(slices, n))) for n in range(1, len(slices)))

def unshred1(slices, corpus, prev_score=None):
  if not prev_score:
    prev_score = evaluate(slices, corpus)

  max_score = prev_score
  best_move = None
  for move, undo in make_moves(slices):
    slices = move(slices)
    score = evaluate(slices, corpus)
    if score > max_score:
      best_move = move
      max_score = score
    slices = undo(slices)
  if best_move:
    slices = best_move(slices)
    return unshred1(slices, corpus, max_score)
  else:
    return slices

def evaluate2(slices, corpus):
  lines = linearize(slices)
  return sum(corpus.W_seq("".join(l)) for l in lines)

def unshred2(slices, corpus, frozen=[]):
  if not slices:
    return frozen

  # brute force the first n slices
  n = 1
  if len(frozen) < n:
    best_slices = None
    best_score = 0
    for i in range(len(slices)):
      new_slices = unshred2(slices[:i] + slices[i+1:], corpus, frozen + [slices[i]])
      score = evaluate3(new_slices, corpus)
      for l in linearize(new_slices):
        print l
      print score
      if score > best_score:
        print "winner"
        best_slices = new_slices
        best_score = score
    return best_slices

  # greedily pick the remaining slices
  #slices.sort(key=lambda slice: corpus.W_seq(serialize(frozen + [slice])), reverse=True)
  slices.sort(key=lambda slice: evaluate2(frozen + [slice], corpus), reverse=True)
  frozen.append(slices[0])
  return unshred2(slices[1:], corpus, frozen)

def evaluate3(slices, corpus):
  return corpus.W_seq(serialize(slices))

def unshred3(slices, corpus, frozen=[]):
  if not slices:
    return frozen

  # brute force the first n slices
  n = 1
  if len(frozen) < n:
    return max((
      unshred2( slices[:i] + slices[i+1:], corpus, frozen + [slices[i]] )
      for i in range(len(slices))
    ), key=lambda slices: evaluate3(slices, corpus))

  slices.sort(key=lambda slice: evaluate2(frozen + [slice], corpus))
  frozen.append(slices.pop())
  return unshred2(slices, corpus, frozen)

def solve_p2_greedy(file):
  lines = [l.lower().split("|")[1:-1] for l in open(file)]
  slices = slice(lines)

  n = 3
  corpus = NgramLetterCorpus(n)
  for fileid in gutenberg.fileids()[:3]:
    corpus.update(gutenberg.raw(fileid))

  slices = unshred3(slices, corpus)
  print "FINAL: "
  for l in linearize(slices):
    print "".join(l)

def solve_all():
  print "Problem 1"
  print "Brute force:"
  solve_p1_brute("p1.txt")
  print "Probabilistic, dictionary-based:"
  solve_p1_prob("p1.txt")
  print "Test Problem Rot 18"
  print "Probabilistic, dictionary-based:"
  solve_p1_prob("test_rot_18.txt")
  print
  print "Problem 2"
  print "Greedy:"
  solve_p2_greedy("p2.txt")

if __name__ == "__main__":
  #solve_all()
  solve_p2_greedy("hard.txt")
