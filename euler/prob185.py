d = []

def numbermind(n):
    for i in range(n):
        d.append([.1 for i in range(10)])

def normalize(v):
    s = sum(v)
    for i in range(len(v)):
        v[i] = float(v[i])/s

def update(s, x):
    if x == 0:
        for i,c in enumerate(s):
            n = int(c)
            d[i][n] = 0
    else:
        for i,c in enumerate(s):
            n = int(c)
            if d[i][n] == 0:
                pass
            elif d[i][n] == 1:
                d[i][n] == 0
            else:
                d[i][n] += x

numbermind(16)

for i in range(100):
    update("5616185650518293",2)
    update("3847439647293047",1)
    update("5855462940810587",3)
    update("9742855507068353",3)
    update("4296849643607543",3)
    update("3174248439465858",1)
    update("4513559094146117",2)
    update("7890971548908067",3)
    update("8157356344118483",1)
    update("2615250744386899",2)
    update("8690095851526254",3)
    update("6375711915077050",1)
    update("6913859173121360",1)
    update("6442889055042768",2)
    update("2321386104303845",0)
    update("2326509471271448",2)
    update("5251583379644322",2)
    update("1748270476758276",3)
    update("4895722652190306",1)
    update("3041631117224635",3)
    update("1841236454324589",3)
    update("2659862637316867",2)
    if i > 20:
        for a in d:
            m = max(a)
            p = a.index(m)
            if m not in a[p+1:]:
                for j in range(10):
                    a[j] = 0 if p != j else 1


for i in range(len(d)):
    normalize(d[i])
answer = []
for a in d:
    #print a
    b = enumerate(a)
    g = max(b, key=lambda x: x[1])
    print a, g[0]
    answer.append(str(g[0]))
print ''.join(answer)

5845859447028557
5845859447028567
5845859447228557
5845859447228567
5845859647028557
5845859647028567
5845859647228557
5845859647228567
5846859447028557
5846859447028567
5846859447228557
5846859447228567
5846859647028557
5846859647028567
5846859647228557
5846859647228567
