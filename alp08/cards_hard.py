import sys, copy

class Position:
    def __init__ (self):
        self.color = 0
        self.value = [0, 0, 0, 0]
        self.empty = True
        self.visited = False
        self.component = -1

class Card_arr:
    def __init__ (self, colors):
        self.colors = colors
        self.values = []
        self.visited = []
        self.component = []

class Card:
    def __init__ (self, R, C, colors):
        self.R = R # rows
        self.C  = C # collums
        self.arr = Card_arr(colors)
    def make2d(self):
        new_colors = [[0] * self.C for i in range(self.R)]
        for i in range(self.R):
            for j in range(self.C):
                new_colors[i][j] = self.colors[i * self.C + j]
        self.arr.colors = copy.deepcopy(new_colors)
        self.arr.values = [[0] * self.C for i in range(self.R)]
        self.arr.visited = [[False] * self.C for i in range(self.R)]
        self.arr.component = [[-1] * self.C for i in range(self.R)]
    def add_values():
        for i in range(self.R):
            for j in range(self.C):
                if self.arr.visited


moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
def BFS(arr, visited, pos, color, component, find_poi):
    queue = [pos]
    arr[pos[0]][pos[1]].visited = True
    score = 0
    if find_poi:
        poi = [] # points of interest
    while queue:
        score += 1
        pos = queue.pop(0)
        arr[pos[0]][pos[1]].component = component
        for i in moves:
            np = [pos[0] + i[0], pos[1] + i[1]]
            if np[0] < 0 or np[1] < 0 or np[0] >= len(arr) or np[1] >= len(arr[0]):
                continue
            if not arr[np[0]][np[1]].visited and arr[np[0]][np[1]].color == color:
                queue.append(np)
                arr[np[0]][np[1]].visited = True
            if find_poi and not arr[np[0]][np[1]].visited and arr[np[0]][np[1]].empty:
                poi.append(np)
                visited[np[0]][np[1]] = True
    if find_poi:
        return poi, score
    else:
        return score

# reading input
filename = sys.argv[1]
with open(filename) as file:
    r, c = map(int, file.readline().split())
    m, n = map(int, file.readline().split()) # cards on table, cards in hand
    arr = [[Position(i, j) for j in range(c)] for i in range(r)]

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

cards = []
for card in temp_cards:
    cards.append(copy.deepcopy(card))
    cards[-1].make2d()

    temp_colors = []
    for i in range(len(card.colors) - 1, -1, -1):
        temp_colors.append(card.colors[i])
    cards.append(Card(card.R, card.C, temp_colors))
    cards[-1].make2d()

    temp_colors = []
    for i in range(card.C):
        for j in range(card.R - 1, -1, -1):
            temp_colors.append(card.colors[j * card.C + i])
    cards.append(Card(card.R, card.C, temp_colors))
    cards[-1].R, cards[-1].C = cards[-1].C, cards[-1].R
    cards[-1].make2d()

    temp_colors = []
    for i in range(card.C - 1, -1, -1):
        for j in range(card.R):
            temp_colors.append(card.colors[j * card.C + i])
    cards.append(Card(card.R, card.C, temp_colors))
    cards[-1].R, cards[-1].C = cards[-1].C, cards[-1].R
    cards[-1].make2d()


# add potential value for empty points

visited = [[False] * c for i in range(r)]
for i in range(r):
    for j in range(c):
        if not arr[i][j].empty and arr[i][j].color != 0 and not arr[i][j].visited:
            poi, score = BFS(arr, visited, [i, j], arr[i][j].color, True)
            for i in poi:
                arr[i[0]][i[1]].visited = False
                arr[i[0]][i[1]].value[color - 1] = score
            

poi = [[] for i in range(4)]
for c in range(4):
    for i in range(r):
        for j in range(c):
            if arr[i][j].value[c] > 0:
                poi[c].append([i, j])


# pick a card
def by_place():
    for i in range(r):
        for j in range(c):
            for card in cards:
                fit = True
                for ic in range(card.R):
                    for jc in range(card.C):
                        if not arr[i + ic][j + jc].empty:
                            fit = False
                            break
                    if not fit:
                        break
                if not fit:
                    continue

                neighbour = False
                if i - 1 >= 0 and not neigbour:
                    for k in range(card.C):
                        if not arr[i - 1][j + k].empty():
                            neigbour = True
                            break
                if i + card.R < r and not neigbour:
                    for k in range(card.C):
                        if not arr[i + card.R][j + k].empty():
                            neigbour = True
                            break
                if j - 1 > 0 and not neigbour:
                    for k in range(card.R):
                        if not arr[i + k][j - 1].empty():
                            neigbour = True
                            break
                if j + card.C < c and not neigbour:
                    for k in range(card.R):
                        if not arr[i + k][j + card.C].empty():
                            neigbour = True
                            break
                if not neighbour:
                    continue

                for ic in range(card.R):
                    for jc in range(card.C):
                        pos = [i + ic, j + jc]
                        color = arr[pos[0]][pos[1]].color
                        if not arr[pos[0]][pos[1]].visited and arr[pos[0]][pos[1]].value[color - 1] > 0:


                    


def by_card_parts():
    for card in cards:
        for i in range(card.R):
            for j in range(card.C):
                if j > 0 and i > 0 and i < card.R - 1:
                    j = card.C - 1
                if card.color[i][j] == 0:
                    continue
                for p in poi[card.colors[i][j]]:
                    fit = True
                    for ic in range(card.R):
                        if not fit:
                            break
                        for jc in range(card.C):
                            if not arr[][].empty():
                                fit = False
                                break
                    if not fit:
                        continue
                
