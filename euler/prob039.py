import math

def num_right_triangles(p):
    num = 0
    for a in range(1,p//4+1):
        for b in range(a+1,(p-a)//2+1):
            c = math.sqrt(a*a+b*b)
            if a+b+c == p:
                num += 1
    return num

if __name__ == "__main__":
    arg = 1
    max = 0

    for i in range(1000):
        n = num_right_triangles(i)
        if n > max:
            arg = i
            max = n

    print(arg, max)
