import sys

class Position:
    def __init__ (self, x, y):
        self.x = x # row position
        self.y = y # col position
        self.color = 0
        self.value = 0
        self.empty = True

class Card:
    def __init__ (self, R, C, colors):
        self.R = R # rows
        self.C  = C # collums
        self.colors = colors

def PM(arr):
    for i in arr:
        for j in i:
            print(j, end = " ")
        print()

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
    cards.append(card)

    temp_colors = []
    for i in range(len(card.colors) - 1, -1, -1):
        temp_colors.append(card.colors[i])
    cards.append(Card(card.R, card.C, temp_colors))

    temp_colors = []
    for i in range(card.C):
        for j in range(card.R - 1, -1, -1):
            temp_colors.append(card.colors[j * card.C + i])
    cards.append(Card(card.R, card.C, temp_colors))

    temp_colors = []
    for i in range(card.C - 1, -1, -1):
        for j in range(card.R):
            temp_colors.append(card.colors[j * card.C + i])
    cards.append(Card(card.R, card.C, temp_colors))

# vstup je přečtený, projít a určit potenciální hodnoty po přidání karty
