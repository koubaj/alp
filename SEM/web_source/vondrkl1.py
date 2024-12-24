import base as BASE
import copy, random, time, sys, os
from PIL import Image, ImageDraw


#basic cards with colors 1 and 2
#note that Brute can provide you also other cards!

def getPossiblePositions(heightC, widthC):
    points = []
    for r in range(R - heightC + 1):
        for c in range(C - widthC + 1): 
            def a():
                isValid = False
                for rm in range(heightC):
                    for cm in range(widthC):
                        if field[r + rm][c + cm] > -1:
                            return
                        if  (rm == 0            and r > 0           and field[r + rm - 1][c + cm] > -1) or \
                            (rm == heightC - 1  and r < R - heightC and field[r + rm + 1][c + cm] > -1) or \
                            (cm == 0            and c > 0           and field[r + rm][c + cm - 1] > -1) or \
                            (cm == widthC - 1   and c < C - widthC  and field[r + rm][c + cm + 1] > -1):
                            isValid = True
                if isValid:
                    points.append([r, c])
            a()
    return(points)

def fill(x, y, new, mmatrix):
    number = 1
    stack = [(x, y)]
    old = mmatrix[x][y]
    mmatrix[x][y] = new
    if old == new:
        return None, 0

    while (len(stack) != 0):
        x, y = stack.pop()
        move = [(0, -1),(0, 1),(-1, 0),(1, 0)]
        for i in move:
            nx, ny = x + i[0], y + i[1]
            if nx < len(mmatrix) and ny < len(mmatrix[0]) and ny > -1 and nx > -1 and mmatrix[nx][ny] == old:
                stack.append((nx, ny))
                mmatrix[nx][ny] = new
                number += 1
    return mmatrix, number

def fillCount(x, y, new, matrix):
    matrix, number = fill(x, y, new, matrix)
    return number

def writeInFieldG(imp):
    if imp == []:
        return None
    ri, ci, mat = imp
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            field[ri + i][ci + j] = mat[i][j]

class Card:
    def __init__(self, matrixi):
        self.R = len(matrixi)
        self.C = len(matrixi[0])
        self.matrix = matrixi
            
        self.rotations = []
        self.rotations.append(self.matrix)
        for k in range(3):
            new_matrix = [[self.rotations[k][j][i] for j in range(len(self.rotations[k]))] for i in range(len(self.rotations[k][0])-1,-1,-1)]
            self.rotations.append(new_matrix)

    def writeInField(self, ri, ci, maxsize, rotation = 0):
        for i in range(self.R):
            for j in range(self.C):
                field[ri + i][ci + j] = self.rotations[rotation][i][j]

    def getMatrix(self):
        return self.matrix

    
    
    def getBestPos(self):
        listpos = dict()
        listpos[self.R] = getPossiblePositions(self.R, self.C)
        if not self.R == self.C:
            listpos[self.C] = getPossiblePositions(self.C, self.R)

        fieldForNow = [row[:] for row in field]

        best = [0, -1, -1, -1]

        for r in range(len(self.rotations)):
            rotation = self.rotations[r]
            rr, cr = len(rotation), len(rotation[0])
            positions = listpos[len(rotation)]
            startPoint = []
            matrixCopy = [row[:] for row in rotation]

            for i in range(rr):
                for j in range(cr):
                    if matrixCopy[i][j] > 0:
                        matrixCopy, count = fill(i, j, 0, matrixCopy)
                        startPoint.append([i, j, count])

            for position in positions:
                for i in range(rr):
                    for j in range(cr):
                        fieldForNow[position[0] + i][position[1] + j] = rotation[i][j]
                scount = 0
                for k in startPoint:
                    count = fillCount(k[0] + position[0], k[1] + position[1], 0, fieldForNow)
                    if count > k[2]:
                        scount += count
                    if scount >= best[0]:
                        best = [scount, position[0], position[1], r]
                fieldForNow = [row[:] for row in field]

        if best[3] == -1:
            return [-1]

        return [best[0], best[1], best[2], self.rotations[best[3]]]

R, C, field = 0, 0, []

class Player(BASE.BasePlayer):
    def __init__(self, login, boardRows, boardCols, cardsAtHand):
        super().__init__(login, boardRows, boardCols, cardsAtHand)
        self.playerName = "Wowbagger, the Infinitely Prolonged"
        global R 
        R = boardRows
        global C 
        C = boardCols
        global field
        self.cardsMy = list()
        field = [[-1 for _ in range(C)] for _ in range(R)]
        for card in cardsAtHand:
            self.cardsMy.append(Card(card))
        self.first = True

    def play(self, newCardOnDesk):
        if len(self.cardsMy) == 0:
            return []
        writeInFieldG(newCardOnDesk)

        if len(newCardOnDesk) == 3:
            self.cardsOnDesk += [ newCardOnDesk ]


        best = -1
        card = 0
        for i in range(len(self.cardsMy)):
            result = self.cardsMy[i].getBestPos()
            if result[0] > best:
                best = result[0]
                card = i
                ri, ci, mat = result[1], result[2], result[3]

        if best == -1 and not self.first:
            return[]
        elif best == -1 and self.first:
            cardindx = random.randint(0, len(self.cardsAtHand)-1)  #random index of a card
            card = self.cardsAtHand[cardindx]
            cardRows = len(card)
            cardCols = len(card[0])
            row = random.randint(0, self.boardRows-cardRows-1) 
            col = random.randint(0, self.boardCols-cardCols-1)
            self.cardsAtHand = self.cardsAtHand[:cardindx] + self.cardsAtHand[cardindx+1:]  #remove selected card so its not used in future
            self.cardsMy.pop(cardindx)
            self.cardsOnDesk += [ [row, col, card ] ]
            writeInFieldG([row, col, card])
            self.first = False
            return [row, col, card ]



            matt = self.cardsMy.pop()
            matt = matt.getMatrix()
            self.first = False
            self.cardsOnDesk += [ [0, 0, matt ] ]
            writeInFieldG([0, 0, matt])
            return[0, 0, matt]
        else:
            self.cardsMy.pop(card)
            self.first = False
            print(best)
            #return[]
            self.cardsOnDesk += [ [ri, ci, mat ] ]
            writeInFieldG([ri, ci, mat])
            return[ri, ci, mat]