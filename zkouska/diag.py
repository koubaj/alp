import sys
filename, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

matrix = []
with open(filename) as file:
    for line in file:
        matrix.append(list(map(int, line.split())))

r, c = len(matrix), len(matrix[0])

def isok(i, j):
    if matrix[i][j] <= b and matrix[i][j] >= a:
        return True
    else:
        return False
maxim = [-1, 0, 0]
for i in range(r):
    for j in range(c):
        if isok(i, j):
            np = [i + 1, j + 1]
            now = [1, i, j]
            while np[0] < r and np[1] < c and np[0] >= 0 and np[1] >= 0:
                if isok(np[0], np[1]):
                    now[0] += 1
                else:
                    break
                np[0] += 1
                np[1] += 1
            if now[0] > maxim[0]:
                maxim = now

            np = [i + 1, j - 1]
            now = [1, i, j]
            while np[0] < r and np[1] < c and np[0] >= 0 and np[1] >= 0:
                if isok(np[0], np[1]):
                    now[0] += 1
                else:
                    break
                np[0] += 1
                np[1] -= 1
            if now[0] > maxim[0]:
                maxim = now

if maxim[0] == -1:
    print("NOSOLUTION")
else:
    print(maxim[1], maxim[2], maxim[0])
