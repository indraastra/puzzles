import util

_sum = sum

r4 = list(range(1,5))
peter_distribution = {}
for a in r4:
    for b in r4:
        for c in r4:
            for d in r4:
                for e in r4:
                    for f in r4:
                        for g in r4:
                            for h in r4:
                                for i in r4:
                                    sum = a + b + c + d + e + f + g + h + i
                                    count = peter_distribution.get(sum, 0)
                                    peter_distribution[sum] = count + 1

util.normalize(peter_distribution)
print(peter_distribution)

r6 = list(range(1,7))
colin_distribution = {}
for a in r6:
    for b in r6:
        for c in r6:
            for d in r6:
                for e in r6:
                    for f in r6:
                        sum = a + b + c + d + e + f
                        count = colin_distribution.get(sum, 0)
                        colin_distribution[sum] = count + 1

util.normalize(colin_distribution)
print(colin_distribution)

def P_P_greater_c(c):
    sum = 0
    for p in peter_distribution:
        if p > c:
            sum += peter_distribution[p]
    return sum

def P_C_greater_p(p):
    sum = 0
    for c in colin_distribution:
        if c > p:
            sum += colin_distribution[c]
    return sum

def P_c(c):
    return colin_distribution.get(c, 0)

def P_p(p):
    return colin_distribution.get(p, 0)

# one method is to say that 
# P(Sum_P > Sum_C) = SUM_(forall c) P(Sum_C = c) * P(Sum_P > c)

P = 0
for c in colin_distribution:
    P += P_c(c) * P_P_greater_c(c)
print(P)

# alternate method is to compute the joint
joint = {}
for p in peter_distribution:
    for c in colin_distribution:
        joint[(p,c)] = peter_distribution[p] * colin_distribution[c]

P_g = 0
P_l = 0
P_e = 0
for p, c in joint:
    if p < c:
        P_l += joint[(p,c)]
    elif p == c:
        P_e += joint[(p,c)]
    elif p > c:
        P_g += joint[(p,c)]
print(P_g)
