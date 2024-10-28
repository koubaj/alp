def matrix_trace(matrix):
    out = matrix[0][0]
    i = 1
    j = 1
    while i < len(matrix):
        out *= matrix[i][j]
        i += 1
        j += 1
    return out


a = [[5, 7], [4, 3]]
print(matrix_trace(a))
