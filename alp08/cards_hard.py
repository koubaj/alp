import sys

class Card:
    def __init__ (self, R, C, arr):
        self.R = R
        self.C  = C
        self.arr = arr

def PM(arr):
    for i in arr:
        for j in i:
            print(j, end = " ")
        print()

filename = sys.argv[1]
with open(filename) as file:
    r, c = map(int, file.readline().split())
    m, n = map(int, file.readline().split())

    arr = [[5] * c for i in range(r)]
    for i in range(m):
        temp = list(map(int, file.readline().split()))
        ri, ci = temp[:2]
        Ri, Ci = temp[2:4]
        colors = temp[4:]
        for i in range(Ri):
            for j in range(Ci):
                arr[ri + i][ci + j] = colors[i*j + j]
    cards = []
    for i in range(n):
        temp = list(map(int, file.readline().split()))
        Ri, Ci = temp[:2]
        colors = temp[2:]
        new = Card(Ri, Ci, colors)
        cards.append(new)

for card in cards:
    c1  = [card[i] for i in range()]
    n1 = Card(card.R, card.C, c1)
    print(card.arr)
    print(c1)
