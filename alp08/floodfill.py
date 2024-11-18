m=[
[0,0,1,0,0,1,0,0,0,0],
[0,0,1,0,0,1,0,0,0,0],
[0,0,1,1,0,1,0,0,0,1],
[0,0,1,0,0,0,1,0,1,0],
[0,0,1,0,0,0,0,1,0,0],
[0,0,1,1,0,1,0,0,0,0],
[0,0,1,0,1,1,1,1,0,0],
[0,0,1,0,0,1,0,1,1,1],
[0,0,1,0,0,1,0,0,0,0],
[0,0,1,0,0,1,0,0,0,0] ]

def PM(arr):
    for i in arr:
        for j in i:
            print(j, end=" ")
        print()

PM(m)
print()

r = len(m)
s = len(m[0])
start = [0, 3]
stack = [start]
moves = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

while stack:
    pos = stack.pop()
    for i in moves:
        newpos = [pos[0] + i[0], pos[1] + i[1]]
        if newpos[0] >= 0 and newpos[1] >= 0 and newpos[0] < r and newpos[1] < s:
            if m[newpos[0]][newpos[1]] == 0:
                m[newpos[0]][newpos[1]] = 2
                stack.append([newpos[0], newpos[1]])
PM(m)
