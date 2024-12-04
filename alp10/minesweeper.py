import sys

class Place():
    def __init__ (self, num):
        self.num = num 
        self.now = -1 
        self.mine = True 
        self.done = False
        self.neighbours = []

filename = sys.argv[1]
arr = []
with open(filename) as file:
    for count, line in enumerate(file):
        arr.append([])
        for num in line.split():
            arr[count].append(Place(int(num)))
r = len(arr)
c = len(arr[0])

def print_res():
    for i in arr:
        for j in i:
            print("X" if j.mine else ".", end = "")
        print()

moves = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
for i in range(r):
    for j in range(c):
        arr[i][j].neighbours = [[i, j]]
        for m in moves:
            np = [i + m[0], j + m[1]]
            if np[0] >= 0 and np[1] >= 0 and np[0] < r and np[1] < c:
                arr[i][j].neighbours.append([np[0], np[1]])
        arr[i][j].now = len(arr[i][j].neighbours)

for i in range(r):
    for j in range(c):
        if arr[i][j].num == len(arr[i][j].neighbours):
            for np in arr[i][j].neighbours:
                arr[np[0]][np[1]].mine = True
                arr[np[0]][np[1]].done = True

        if arr[i][j].num == 0 and not arr[np[0]][np[1]].done:
            for np in arr[i][j].neighbours:
                arr[np[0]][np[1]].mine = False
                arr[np[0]][np[1]].done = True
            for np in arr[i][j].neighbours:
                for nnp in arr[np[0]][np[1]].neighbours:
                    arr[nnp[0]][nnp[1]].now -= 1

def check_ok(pos):
    for np in arr[pos[0]][pos[1]].neighbours:
        score = 4 + (np[0] - pos[0]) * 3 + (np[1] - pos[1])
        if score == 1 and pos[1] == c - 1:
            score = 0
        if pos[0] == r-1 and (score == 3 or (pos[1] == c-1 and score == 4)):
            score = 0
        if arr[np[0]][np[1]].now - arr[np[0]][np[1]].num > score or arr[np[0]][np[1]].now < arr[np[0]][np[1]].num:
            return False
    return True

def recursion(arr, pos):
    np = [pos[0] + ((pos[1] + 1) // c), (pos[1] + 1) % c]
    if pos[0] == r:
        print_res()
        quit()

    if check_ok(pos):
        recursion(arr, np)
    if not arr[pos[0]][pos[1]].done:
        arr[pos[0]][pos[1]].mine = False
        for npp in arr[pos[0]][pos[1]].neighbours:
            arr[npp[0]][npp[1]].now -= 1

        if check_ok(pos):
            recursion(arr, np)
        
        for npp in arr[pos[0]][pos[1]].neighbours:
            arr[npp[0]][npp[1]].now += 1
        arr[pos[0]][pos[1]].mine = True

recursion(arr, [0, 0])
