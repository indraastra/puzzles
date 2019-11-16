import psyco

sum = 1
for i in range(1,(1001+1)/2):
    sum += (2*i+1)**2
    sum += 4*i**2-2*i+1
    sum += 4*i**2+1
    sum += 4*i**2+2*i+1

print sum
