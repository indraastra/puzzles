onetohundred = range(1,101)
sumsquares = sum(i**2 for i in onetohundred)
squaresum  = sum(onetohundred) ** 2
print(squaresum - sumsquares)
