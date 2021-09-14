import cProfile

def isInc(l):
    p = -1
    for i in l:
        if p > i:
            return False
        p = i
    return True

def isDec(l):
    p = 10
    for i in l:
        if p < i:
            return False
        p = i
    return True

def isBouncy(n):
    return not isInc(n) and not isDec(n)

def nextInc(n):
    n += 1
    l = list(map(int,list(str(n))))
    if isInc(l):
        return n
    else:
        p = -1
        for i,e in enumerate(l):
            if p > e:
                break
            else:
                p = e
        i -= 1
        m = l[i]
        l[i:] = [m]*(len(l)-i)
        return int(''.join(map(str,l)))

def nextDec(n):
    n += 1
    l = list(map(int,list(str(n))))
    if isDec(l):
        return n
    else:
        p = 10
        j = -1
        for i,e in enumerate(l):
            if p < e:
                break
            if p > e:
                p = e
                j = i
        i = j
        l[i] += 1
        l[i+1:] = [0]*(len(l)-i-1)
        return int(''.join(map(str,l)))

def nextBouncy(n):
    n += 1
    l = list(map(int,list(str(n))))
    if isBouncy(l):
        return n
    else:
        if isInc(l):
            n += 9
            n -= n % 10
            return n
        else:
            if l[-2] == 9:
                n += 9
                l = list(map(int,list(str(n))))
            l[-1] = l[-2]+1
            n = int(''.join(map(str,l)))
            if isInc(l):
                return nextBouncy(n)
            else:
                return n

def start():
    countNonBouncy = 99
    i = 100
    prevBouncy = True
    while i < 10**8:
        if prevBouncy:
            j = min(nextInc(i),nextDec(i))
            prevBouncy = False
        else:
            j = nextBouncy(i)
            countNonBouncy += (j-i)
            prevBouncy = True
        i = j
    print(countNonBouncy)

if __name__ == "__main__":
    cProfile.run("start()")
