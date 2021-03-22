def collatzSequence(n):
    s = 1
    while n > 1:
        if n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1
        s += 1
    return s

if __name__ == "__main__":
    max = 0
    argmax = 0
    for i in range(10**6,1,-1):
        l = collatzSequence(i)
        if l > max:
            max = l
            argmax = i
    print(argmax)
