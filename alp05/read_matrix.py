def read_matrix(matrix):
    out = ""
    for i in matrix:
        for j in i:
            out += str(j)
    return out

a=[["A","B","C"], ["D","E","F"]]
print(read_matrix(a))
