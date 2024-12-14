import sys

def to_letter(a):
    return chr(a + 65)

def make_string(arr):
    s = ""
    for i in arr:
        for j in i:
            s += str(j)
        s += "."
    s[:-1]
    return s

filename = sys.argv[1]
start = []
with open(filename) as file:
    for line in file:
        start.append(list(map(int, line.split())))
start.append([])
n = len(start)
m = len(start[0])
for i in range(n - 1):
    for j in range(m):
        start[i][j] -= 1
start = make_string(start)

states = {}
states[start] = ["", ""]

end = ""
for i in range(n-1):
    for j in range(m):
        end += str(i)
    end += "."
end += "."

queue = [start]
pos = start
while pos != end:
    pos = queue.pop(0)
    
    # convert string into 2d array
    arr = [[]]
    n_pos = 0
    for c in pos:
        if c == ".":
            n_pos += 1
            arr.append([])
        else:
            arr[n_pos].append(int(c))
    arr.pop()

    # create new states
    np = []
    for i in range(n):
        if len(arr[i]) < m:
            np.append(i)
    for i in range(n):
        if not arr[i]:
            continue
        for j in np:
            if i == np:
                continue
            arr[j].append(arr[i].pop())
            t = make_string(arr)
            if t not in states:
                states[t] = [pos, to_letter(i) + to_letter(j)]
                queue.append(t)
            arr[i].append(arr[j].pop())

# backtrack
ans = []
while pos != start:
    ans.append(states[pos][1])
    pos = states[pos][0]
for i in reversed(ans):
    print(str(i), end = " ")
print()
