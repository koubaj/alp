import sys

class Line():
    def __init__(self, x, y, a, b):
        self.start = [x, y]
        self.end = [a, b]

lines = []
filename = sys.argv[1]
with open(filename) as file:
    for line in file:
        temp = (list(map(int, line.split())))
        lines.append(Line(temp[0], temp[1], temp[2], temp[3]))
        lines.append(Line(temp[2], temp[3], temp[0], temp[1]))

graph = [[[] for j in range(101)] for i in range(101)]
for i in lines:
    graph[i.start[0]][i.start[1]].append(i.end)


comp = [[-1 for j in range(101)] for i in range(101)]
cp = 0

def bfs(graph, comp, pos, cp):
    queue = [pos]
    nums = 0
    while queue:
        pos = queue.pop(0)
        for np in graph[pos[0]][pos[1]]:
            if comp[np[0]][np[1]] == -1:
                nums += 1
                comp[np[0]][np[1]] = cp
                queue.append(np)
    return cp, nums

gnum = 0
for i in range(101):
    for j in range(101):
        cp, num = bfs(graph, comp, [i, j], cp)
        if num > 0:
            cp += 1
        if i == 0 and j == 0:
            gnum = num
print(cp, gnum)
