O = (0, 0)

def area(p1, p2, p3):
    a, b, c = p1, p2, p3
    return abs(( a[0] * ( b[1] - c[1] ) + b[0] * ( c[1] - a[1] ) + c[0] * ( a[1] - b[1] )) / float(2))

if __name__ == "__main__":
    count = 0
    for line in open("triangles.txt"):
        triangle = [int(c) for c in line.strip().split(",")]
        a0, a1, b0, b1, c0, c1 = triangle
        a = (a0, a1)
        b = (b0, b1)
        c = (c0, c1)
        triangle = [(a[0], a[1]),
                    (b[0], b[1]),
                    (c[0], c[1])]
        if area(a, b, c) == (area(a, b, O) + area(a, O, c) + area(O, b, c)):
            count += 1
    print count
