import psyco
import re
import random
import util

wordre = "[a-zA-Z]+"

words = set([w.strip().lower() for w in open("/etc/dictionaries-common/words").readlines()])
ciphertext = [int(i) for i in open("cipher1.txt").read().split(",")]

def decode(ciphertext, key):
    plaintext = ciphertext[:]
    for i, c in enumerate(ciphertext):
        n = i % len(key)
        plaintext[i] = ciphertext[i] ^ key[n]
    return plaintext

def search(ciphertext):
    for i in range(97,123):
        for j in range(97,123):
            for k in range(97,123):
                plaintext = decode(ciphertext, (i,j,k))
                plainstr = util.ints2str(plaintext)
                plainwords = re.findall(wordre, plainstr)
                tried = 0.0
                found = 0.0
                while tried < 20:
                    w = random.choice(plainwords)
                    if len(w) >= 3:
                        tried += 1
                    else:
                        continue
                    if w.lower() in words:
                        found += 1
                if tried and found/tried >= .75:
                    return plaintext

print sum(search(ciphertext))
