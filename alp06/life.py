import copy
def life(a):
    newa = copy.deepcopy(a)
    for r in range(len(a)):
        for c in range(len(a[r])):
            n = 3
            if n == 3:
                newa[r][c] = 1
            elif n == 2:
                pass
            else:
                newa[r][c] = 0
    return newa
