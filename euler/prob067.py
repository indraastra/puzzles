
triangle = [list(map(int, line.strip().split())) for line in open("triangle.txt").readlines()]

results = []

for i in range(len(triangle)-1, -1, -1):
    row = [n for n in triangle[i]]
    if i != len(triangle)-1:
        next = results[0]
        row = [r+max(next[j],next[j+1]) for j,r in enumerate(row)]
    results.insert(0, row)

print(results[0][0])
