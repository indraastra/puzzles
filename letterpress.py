from collections import Counter

dict = "/usr/share/dict/words"
min_length = 5

words = [line.strip().lower() for line in open(dict, "r") if len(line.strip()) >= min_length]
counters = [Counter(word) for word in words]
print "loaded dictionary"

while True:
  letters = Counter(raw_input("letters > ").lower())

  valid_words = []
  for (word, counter) in zip(words, counters):
    if (counter & letters) == counter:
      valid_words.append(word)
  
  valid_words.sort(key=len, reverse=True)
  for word in valid_words[:100]:
    print "".join(word)
