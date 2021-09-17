def digital_sum(x):
    return sum(map(int, str(x)))


print(max(digital_sum(a**b) for a in range(100) for b in range(100)))
