import psyco

S = [i ** 2 for i in range(1, 101)]
c = 50
min = sum(S[:50])
max = sum(S[50:])
S.reverse()

print "S", S
print "c", c
print "min", min
print "max", max
#S = reversed([1,3,6,8,10,11])
#c = 3
#min = 10
#max = 29

def num_ways(i, c, S):
    if i == 0 or c == 0 or not S:
        if i == 0 and c == 0:
            return 1
        else:
            return 0
    else:
        if S[0] <= i:
            a = num_ways(i - S[0], c - 1, S[1:])
            if a > 1:
                return 100
            else:
                return a + num_ways(i, c, S[1:])
            #return num_ways(i - S[0], c - 1, S[1:]) + \
            #       num_ways(i, c, S[1:])
        else:
            return num_ways(i, c, S[1:])

if __name__ == "__main__":
    total = 0
    #for i in range(max, min-1, -1):
    #    if i % 10000 == 0:
    #        print i
    #    if num_ways(i, c, S) == 1:
    #        print i
    #        total += i
    print num_ways(42925, c, S)
    print "TOTAL:", total
