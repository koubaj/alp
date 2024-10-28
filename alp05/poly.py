def poly(poly, x):
    out = 0
    for count, i in enumerate(poly):
        out += i * (x**count)
    return out

def sumPoly(p1, p2):
    out = [0] * max(len(p1), len(p2))
    for i in range(len(out)):
        out[i] = (p1[i] if i < len(p1) else 0) + (p2[i] if i < len(p2) else 0)
    return out

def mulPoly(p1, p2):
    out = [0] * (len(p1) + len(p2) - 1)
    for ci, i in enumerate(p1):
        for cj, j in enumerate(p2):
            out[ci + cj - 1] += i * j
    return out




p1 = (5, 4, 7) # 5 + 4x + 7x**2
p2 = (0, 1, 3, -2) # x + 3x**2 - 2x**3
#print(poly(p1, 2))
#print(sumPoly(p1, p2))
print(mulPoly(p1, p2))
