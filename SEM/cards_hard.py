import sys, copy

class Position:
    def __init__ (self):
        self.color = 0
        self.value = 0
        self.empty = True
        self.visited = False
        self.component = -1
        self.neighbour = False

class Card_position:
    def __init__ (self):
        self.color = 0
        self.value = 0
        self.visited = False
        self.component = -1

class Card:
    def __init__ (self, R, C, colors):
        self.R = R # rows
        self.C  = C # collums
        self.arr = colors 
    def make2d(self, compc):
        temp_colors = copy.deepcopy(self.arr)
        self.arr = [[Card_position() for _ in range(self.C)] for _ in range(self.R)]
        for i in range(self.R):
            for j in range(self.C):
                self.arr[i][j].color = temp_colors[i * self.C + j]

        for i in range(self.R):
            for j in range(self.C):
                if not self.arr[i][j].visited and self.arr[i][j].color != 0:
                    poi, score, compc = BFS(self.arr, [i, j], self.arr[i][j].color, compc)
                    for k in poi:
                        self.arr[k[0]][k[1]].value = score
        return compc


moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
def BFS(arr, pos, color, component):
    queue = [pos]
    arr[pos[0]][pos[1]].visited = True
    score = 0
    poi = [] # points of interest
    while queue:
        pos = queue.pop(0)
        score += 1
        arr[pos[0]][pos[1]].component = component
        poi.append(pos)
        for i in moves:
            np = [pos[0] + i[0], pos[1] + i[1]]
            if np[0] < 0 or np[1] < 0 or np[0] >= len(arr) or np[1] >= len(arr[0]):
                continue
            if not arr[np[0]][np[1]].visited and arr[np[0]][np[1]].color == color:
                queue.append(np)
                arr[np[0]][np[1]].visited = True
    return poi, score, component + 1

# reading input
filename = sys.argv[1]
with open(filename) as file:
    r, c = map(int, file.readline().split())
    m, n = map(int, file.readline().split()) # cards on table, cards in hand
    arr = [[Position() for j in range(c)] for i in range(r)]

    for i in range(m):
        temp = list(map(int, file.readline().split()))
        ri, ci = temp[:2]
        Ri, Ci = temp[2:4]
        colors = temp[4:]
        for i in range(Ri):
            for j in range(Ci):
                arr[ri + i][ci + j].color = colors[i*Ci + j]
                arr[ri + i ][ci + j].empty = False

    temp_cards = []
    for i in range(n):
        temp = list(map(int, file.readline().split()))
        Ri, Ci = temp[:2]
        colors = temp[2:]
        temp_cards.append(Card(Ri, Ci, colors))

# rotate cards
compc = 0
cards = []
for card in temp_cards:
    cards.append(copy.deepcopy(card))
    compc = cards[-1].make2d(compc)

    temp_colors = []
    for i in range(len(card.arr) - 1, -1, -1):
        temp_colors.append(card.arr[i])
    cards.append(Card(card.R, card.C, temp_colors))
    compc = cards[-1].make2d(compc)

    temp_colors = []
    for i in range(card.C):
        for j in range(card.R - 1, -1, -1):
            temp_colors.append(card.arr[j * card.C + i])
    cards.append(Card(card.C, card.R, temp_colors))
    compc = cards[-1].make2d(compc)

    temp_colors = []
    for i in range(card.C - 1, -1, -1):
        for j in range(card.R):
            temp_colors.append(card.arr[j * card.C + i])
    cards.append(Card(card.C, card.R, temp_colors))
    compc = cards[-1].make2d(compc)


# add value to points of interest and make a list of them
poi = [[] for i in range(5)]
for i in range(r):
    for j in range(c):
        if not arr[i][j].empty and arr[i][j].color != 0 and not arr[i][j].visited:
            local_poi, score, compc = BFS(arr, [i, j], arr[i][j].color, compc)
            for k in local_poi:
                arr[k[0]][k[1]].value = score
                poi[arr[k[0]][k[1]].color].append([k[0], k[1]])
        # is neighbour
        if arr[i][j].empty:
            is_neighbour = False
            for m in moves:
                np = [i + m[0], j + m[1]]
                if np[0] < 0 or np[1] < 0 or np[0] >= r or np[1] >= c:
                    continue
                if not arr[np[0]][np[1]].empty:
                    is_neighbour = True
                    break
            if is_neighbour:
                arr[i][j].neighbour = True

            
# prefix to find fit? fast
space_prefix = [[0] * c for i in range(r)]
for i in range(r):
    for j in range(c):
        if i > 0:
            space_prefix[i][j] += space_prefix[i-1][j]
        if j > 0:
            space_prefix[i][j] += space_prefix[i][j-1]
        if i > 0 and j > 0:
            space_prefix[i][j] -= space_prefix[i - 1][j - 1]
        if not arr[i][j].empty:
            space_prefix[i][j] += 1

def does_fit(arr, pos, cr, cc, space_prefix):
    fit_val = space_prefix[pos[0] + cr][pos[1] + cc]
    if pos[0] > 0 and pos[1]  > 0:
        fit_val += space_prefix[pos[0] - 1][pos[1] - 1]
    if pos[0] > 0:
        fit_val -= space_prefix[pos[0] - 1][pos[1] + cc]
    if pos[1] > 0:
        fit_val -= space_prefix[pos[0] + cr][pos[1] - 1]
    if fit_val == 0:
        return True
    else:
        return False

# pick a card
max_score = -1
ans = []
for i in range(r):
    for j in range(c):
        for count, card in enumerate(cards):
            if i + card.R - 1 >= r or j + card.C - 1 >= c:
                continue
            if not does_fit(arr, [i, j], card.R - 1, card.C - 1, space_prefix):
                continue

            neighbour = False
            for ic in range(card.R):
                for jc in range(card.C):
                    if jc > 0 and ic > 0 and ic < card.R-1:
                        jc = card.C - 1
                    if arr[i + ic][j + jc].neighbour:
                        neighbour = True
                        break
                if neighbour:
                    break
            if not neighbour:
                continue

            # find score
            used_components = {}
            score = 0
            for ic in range(card.R):
                for jc in range(card.C):
                    if jc > 0 and ic > 0 and ic < card.R-1:
                        jc = card.C - 1
                    if card.arr[ic][jc].color == 0:
                        continue
                    pos = [i + ic, j + jc]
                    for m in moves:
                        np = [pos[0] + m[0], pos[1] + m[1]]
                        if np[0] < 0 or np[1] < 0 or np[0] >= r or np[1] >= c:
                            continue
                        if arr[np[0]][np[1]].color == card.arr[ic][jc].color:
                            if arr[np[0]][np[1]].component not in used_components:
                                score += arr[np[0]][np[1]].value
                                used_components[arr[np[0]][np[1]].component] = True
                            if card.arr[ic][jc].component not in used_components:
                                score += card.arr[ic][jc].value
                                used_components[card.arr[ic][jc].component] = True
            if score > max_score:
                max_score = score
                ans = [i, j, card.R, card.C]
                for ic in range(card.R):
                    for jc in range(card.C):
                        ans.append(card.arr[ic][jc].color)


if max_score == -1:
    print("NOSOLUTION")
else:
    for i in ans:
        print(i, end = " ")
