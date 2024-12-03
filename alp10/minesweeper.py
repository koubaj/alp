import sys

class Place():
    def __init__ (self, num):
        self.num = num
        self.mine = False 
        self.done = False
        self.neighbours = []
        self.n_val = 0

filename = sys.argv[1]
arr = []
with open(filename) as file:
    for count, line in enumerate(file):
        arr.append([])
        for num in line.split():
            arr[count].append(Place(int(num)))
r = len(arr)
c = len(arr[0])

moves = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
for i in range(r):
    for j in range(c):
        arr[i][j].neighbours = [[i, j]]
        for m in moves:
            np = [i + m[0], j + m[1]]
            if np[0] >= 0 and np[1] >= 0 and np[0] < r and np[1] < c:
                arr[i][j].neighbours.append([np[0], np[1]])

        if arr[i][j].num == len(arr[i][j].neighbours):
            for np in arr[i][j].neighbours:
                arr[np[0]][np[1]].mine = True
                arr[np[0]][np[1]].done = True

        if arr[i][j].num == 0:
            for np in arr[i][j].neighbours:
                arr[np[0]][np[1]].done = True

def print_res():
    for i in arr:
        for j in i:
            print("X" if j.mine else ".", end = "")
        print()

def is_ok(pos):
    suma = 0
    for np in arr[pos[0]][pos[1]].neighbours:
        if arr[np[0]][np[1]].mine:
            suma += 1
    if arr[pos[0]][pos[1]].num == suma:
        return True
    else:
        return False

def check_ok(pos):
    if pos[0] > 0:
        if pos[1] > 0:
            if not is_ok([pos[0] - 1, pos[1] - 1]):
                return False
        if pos[1] == c - 1:
            if not is_ok([pos[0] - 1, pos[1]]):
                return False
    if pos[0] == r - 1:
        if pos[1] > 0:
            if not is_ok([pos[0], pos[1] - 1]):
                return False
        if pos[1] == c - 1:
            if not is_ok([pos[0], pos[1]]):
                return False
    return True

cache = {}
def recursion(arr, pos):
    if pos[0] > 0 and False:
        prev = ""
        p = max(pos[1] - 1, 0)
        while p < c:
            prev += "X" if arr[pos[0] - 1][p].mine else "."
            p += 1
        p = 0
        while p < pos[1]:
            prev += "X" if arr[pos[0]][p].mine else "."
            p += 1
        prev += str(pos[0]) + str(pos[1])
        
        if prev in cache:
            print_res()
            return False
        else:
            cache[prev] = True

    np = [pos[0] + ((pos[1] + 1) // c), (pos[1] + 1) % c]
    if pos[0] == r:
        print_res()
        quit()

    if check_ok(pos):
        recursion(arr, np)
    if not arr[pos[0]][pos[1]].done:
        arr[pos[0]][pos[1]].mine = True
        if check_ok(pos):
            recursion(arr, np)
        arr[pos[0]][pos[1]].mine = False

recursion(arr, [0, 0])
