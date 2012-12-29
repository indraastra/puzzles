from collections import Counter

# Command line arguments? Psh.
dict = "/usr/share/dict/words"
min_length = 5

# Clean and canonicalize words, dropping ones that don't meet the minimum length.
words = [line.strip().lower() for line in open(dict, "r") if len(line.strip()) >= min_length]
# Create multisets for each word for later comparison to the multiset of letters.
counters = [Counter(word) for word in words]
print "loaded dictionary"

while True:
  # Multiset representing the usable tiles on the game board.
  letters = Counter(raw_input("letters > ").lower())

  # Find all dictionary words that can be formed using the tiles on the board.
  valid_words = []
  for (word, counter) in zip(words, counters):
    if (counter & letters) == counter:
      valid_words.append(word)
  
  # Sort found words by longest first and output first 100.
  valid_words.sort(key=len, reverse=True)
  for word in valid_words[:100]:
    print "".join(word)
