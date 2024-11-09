def matrix_mul(a, b):
    r = len(b[0])
    s = len(b)
    res = [[0] * r for i in range(s)]

    for i in range(s):
        for j in range(r):
            for k in range(r):
                res[i][j] += a[k][j] * b[i][k]
    return res

def transpose(a):
    r = len(a)
    s = len(a[0])
    res = [[0] * r for i in range(s)]

    for ci, i in enumerate(a):
        for cj, j in enumerate(i):
            res[cj][ci] = j
    return res

a = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
b = [[7, 8, 9], [1, 2, 3]]
print(matrix_mul(a, b))
