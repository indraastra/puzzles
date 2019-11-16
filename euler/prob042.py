import psyco
import util

words = [word.strip()[1:-1] for word in open("words.txt", "r").read().split(",")]

max_length = max(len(w) for w in words)

triangle_numbers = [1]

n = 1
while triangle_numbers[-1] < max_length * 26:
    n += 1
    triangle_numbers.append(n*(n+1)/2)

triangle_numbers = set(triangle_numbers)

num_triangle_words = 0
for w in words:
    i = sum([n - 64 for n in util.str2ints(w)])
    if i in triangle_numbers:
        num_triangle_words += 1

print num_triangle_words
