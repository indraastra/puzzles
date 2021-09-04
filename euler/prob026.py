import util

cycle_lengths = {}

for i in range(2,1000):
    if i in cycle_lengths:
        continue
    elif i % 2 == 0 or i % 5 == 0:
        cycle_lengths[i] = 0
    else:
        l = util.order(10, i)
        m = i
        while m < 1000:
            cycle_lengths[m] = l
            m *= i

print(max(list(cycle_lengths.items()), key=lambda x: x[1])[0])
