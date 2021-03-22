import math

def getNumFactors(n):
    i = 2
    c = 2
    while i < math.sqrt(n):
        if n%i == 0:
            c += 2
        i += 1
    return c

if __name__ == "__main__":
    i = 1
    t = 1
    while True:
        if getNumFactors(t) >= 500:
            print(i, t)
            break
        i += 1
        t += i
