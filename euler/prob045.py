import util

NUM = 100000

def triangles():
    n = 0
    while True:
        yield n * (n + 1) // 2
        n += 1

triangles = set(util.take(NUM, triangles()))

def pentagonals():
    n = 0
    while True:
        yield n * (3 * n - 1) // 2
        n += 1

pentagonals = set(util.take(NUM, pentagonals()))

def hexagonals():
    n = 0
    while True:
        yield n * (2 * n - 1)
        n += 1

hexagonals = set(util.take(NUM, hexagonals()))

print(sorted(triangles.intersection(pentagonals).intersection(hexagonals)))
