from util import is_pandigital

products = set()

for i in range(100):
    for j in range(10000):
        k = i*j
        if is_pandigital(''.join(map(str, (i,j,k)))):
            print(i,j,k)
            products.add(k)

print(sum(products))
