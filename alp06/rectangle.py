import sys, copy

def PM(a):
    for i in a:
        for j in i:
            print(j, end=" ")
        print()

temp = []
filename = sys.argv[1]
with open(filename) as file:
    for line in file:
        temp.append(list(map(int, line.split())))

n = len(temp)
m = len(temp[0])
matrix = [[0] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        matrix[i][j] = 1 if temp[i][j] < 0 else 0

prefix = [[0] * m for _ in range(n)]
for j in range(m):
    suma = 0
    for i in range(n):
        if matrix[i][j] == 1:
            suma += 1
        else:
            suma = 0
        prefix[i][j] = suma

maximum = 0
ans = [0] * 4 # r1, r2, s1, s2
for i in range(n):
    prefix[i].append(-1)
    stack = [-1]
    for j in range(m):
        while prefix[i][j] < prefix[i][stack[-1]]:
            val = (j - stack[-2] - 1) * prefix[i][stack[-1]]
            if val > maximum:
                maximum = val
                ans = [i - (prefix[i][stack[-1]] - 1), i, stack[-2] + 1, j - 1]
            stack.pop()
        stack.append(j)
    while len(stack) > 1:
        val = (m - 1 - stack[-2] - 1) * prefix[i][stack[-1]]
        if val > maximum:
            maximum = val
            ans = [i - (prefix[i][stack[-1]] - 1), i, stack[-2] + 1, m - 1]
        stack.pop()

print(ans[0], ans[2])
print(ans[1], ans[3])
