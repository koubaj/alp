import pickle, glob, os, zlib


files = glob.glob("out.*.p")
games = []
beforeCompression = 0
afterCompression = 0

outfile = "allGames.p"
try:
    os.unlink(outfile)
except:
    print("Cannot delete", outfile, "it does not exists")

for name in files:
    f = open(name,"rb")
    d = pickle.load(f)
    f.close()
    beforeCompression += len(d["html"])
    d["html"] = zlib.compress(d["html"].encode(),9)
    d["htmlCompressed"] = True
    afterCompression += len(d["html"])
    games.append(d)

if len(files) > 0:    
    fo = open(outfile,"wb")
    pickle.dump(games, fo)
    fo.close()

print("Saving", files, "into", outfile)
print("Before compression ", int(beforeCompression/ 1024), "k, after compression ", int(afterCompression/1024), "k ", sep="")
os.system("rm out.*.p")
         
removeComments.py
import tokenize, sys
if len(sys.argv) != 2:
    print("usage: ", sys.argv[0], " <inputile> ")
    quit()

filename = sys.argv[1]

outlines = ''
f = open(filename,"rt")

for toktype, tok, start, end, line in tokenize.generate_tokens(f.readline):
    if toktype != tokenize.COMMENT:
        outlines += " " + tok
f.close()    

print(outlines)    
utils.py

import copy, math, base64, io
from PIL import Image, ImageDraw

__all__=[]
def __dir__():
    return []


#variables for visualization
_colors = {}
_colors[-2] = "#eeeeff" #sunglow
_colors[-1] = "#cccccc" #sunglow
_colors[0] = "#ffffff" #white
_colors[1] = "#947bd3" #medium purple
_colors[2] = "#ff0000" #red
_colors[3] = "#00ff00" #green
_colors[4] = "#0000ff" #blue
_colors[5] = "#566246" #ebony
_colors[6] = "#a7c4c2" #opan
_colors[7] = "#ADACB5" #silver metalic
_colors[8] = "#8C705F" #liver chestnut
_colors[9] = "#FA7921" #pumpkin
_colors[10] = "#566E3D" #dark olive green

_colors[1] = "#636940"
_colors[2] = "#59A96A"
_colors[3] = "#ffdd4a"
_colors[4] = "#fe9000"
_colors[-2] = "#a3d9ff"

def cardSize(card):
    return len(card), len(card[0])

def inBoard(board, row, col):
    rows, cols = cardSize(board)
    return row >= 0 and row < rows and col >=0 and col < cols


def card2matrixString(card):
    line = ""
    for r in range(len(card)):
        for c in range(len(card[r])):
            line += "{} ".format(card[r][c])
        line += "\n"
    return line        

def card2png(card, filename):    
    crows, ccols = cardSize(card)
    matrix = [ [0]*ccols for _ in range(crows) ]
    writeCard(0,0,card, matrix)
    drawMatrix(matrix,filename)


def changeColor(card, oldColor, newColor):
    new = copy.deepcopy(card)
    for row in range(len(new)):
        for col in range(len(new[row])):
            if new[row][col] == oldColor:
                new[row][col] = newColor
    return new


def rotateCard(card):
    rows, cols = cardSize(card)
    newCard = [ [0]*rows for _ in range(cols) ]  #new card has switched rows and cols
    for r in range(rows):
        for c in range(cols):
            newCard[cols-1-c][r] = card[r][c]
    return newCard            


def card2line(card):
    line = ""
    for row in range(len(card)):
        for col in range(len(card[row])):
            if len(line) != 0:
                line += " "
            line += str(card[row][col])
    return line



def printCard(card):
    rows, cols = cardSize(card)
    for row in range(rows):
        for col in range(cols):
            print("{:3d}".format(card[row][col]), end=" ")
        print()



def isFreeSpace(board, row, col, numRows, numCols):
    if not inBoard(board,row, col):
        return False
    if not inBoard(board,row+numRows-1, col+numCols-1):
        return False

    for r in range(numRows):
        for c in range(numCols):
            if board[r+row][c+col] != 0:
                return False
    return True                

def isFreeInField(matrix, row, col, cardRows, cardCols, distanceField):
    if row + cardRows > len(matrix):
        return False

    for r in range(row, row + cardRows):
        if distanceField[r][col] < cardCols:
            return False
#    print("Is free", row, col, "TRUE")
#    printCard(distanceField)
    return True        

def isCardTouching(board, row, col, card):
    cardRows, cardCols = cardSize(card)
    for r in range(cardRows):
        cellRow = r + row
        cellCol = col - 1 #left neighbor
        if inBoard(board, cellRow, cellCol) and board[cellRow][cellCol] != 0:
            return True
        cellCol = cardCols + col #which is alredy right neighbor
        if inBoard(board, cellRow, cellCol) and board[cellRow][cellCol] != 0:
            return True
    for c in range(cardCols):
        cellCol = col + c
        cellRow = row-1
        if inBoard(board, cellRow, cellCol) and board[cellRow][cellCol] != 0:
            return True
        cellRow = row + cardRows #already bottom neighb
        if inBoard(board, cellRow, cellCol) and board[cellRow][cellCol] != 0:
            return True
    return False                


def writeCard(row, col, card, board, writeValue = None, backgroundValue = -1):
        cardRows = len(card)
        cardCols = len(card[0])
        if writeValue == None and not isFreeSpace(board, row, col, cardRows, cardCols):
            return False
            """
                print("Cannot place card", cardRows, "x", cardCols, " at ", row,col, " space is not free! ")
                print("Matrix size", cardSize(board))
                print("matrix:", board)
                a = 1/0
                quit()
            """
        for r in range(cardRows):
            for c in range(cardCols):
                val = card[r][c]
                if val == 0:
                    val = backgroundValue
                if writeValue != None:
                    val = writeValue
                board[r+row][c+col] = val
        return True

             
def isEmptyMatrix(matrix):                
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] != 0:
                return False
    return True            


def floodfill(matrix, startRow, startCol):
    #return list of explored cells and their parents
    colorToExplore = matrix[ startRow ][ startCol ]
    openList = [ [ startRow, startCol ] ]
    explored = {}
    neighbors = [ [-1,0],[1,0],[0,-1],[0,1] ]

    while len(openList):
        row, col = openList.pop()
        if not (row, col) in explored:
            explored[ (row, col) ] = ( row, col )

        for n in neighbors:
            newRow = row + n[0]
            newCol = col + n[1]
            if inBoard(matrix, newRow, newCol) and matrix[newRow][newCol] == colorToExplore:
                if not (newRow, newCol) in explored:
                    openList.append( [ newRow, newCol ] )
                    explored[ (newRow, newCol) ] = ( row, col ) #his parent
    return explored


def identifyCardComponents(card):
    cardRows, cardCols = cardSize(card)
    c2 = copy.deepcopy(card)

    colorComponents = {}
    while True:
        startRow = -1
        startCol = -1
        for r in range(cardRows):
            for c in range(cardCols):
                if c2[r][c] > 0:
                    startRow = r
                    startCol = c
                    break
            if startRow != -1:
                break                    
        if startRow == -1: #no unexplored was not found
            break               
        colorToExplore = c2[ startRow ][ startCol ]                
        if colorToExplore < 0:
            print("colorToExplore=",colorToExplore, " cannot be negative!")
            quit()

        positions = floodfill(c2, startRow, startCol)
        if len(positions) == 0:
            print("error in identifyCardComponents, list of component positions is 0")
            quit()

        for pos in positions:
            c2[ pos[0] ][ pos[1] ] *= -1  #1 -> -1, 2 -> -2 etc.., so its ignored by subsequent search
        if colorToExplore not in colorComponents:
            colorComponents[ colorToExplore ] = []

        colorComponents[ colorToExplore ].append( list(positions)[0] )
    return colorComponents


def getAllPlacements(matrix, card, getComponents = None, isFreeDict = None, isCardInTouchDict = None, distanceField = []):
    if isFreeDict == None:
        isFreeDict = {}
    if isCardInTouchDict == None:
        isCardInTouchDict = {}

    cardRows, cardCols = cardSize(card)
    isEmpty = isEmptyMatrix(matrix)
    res = []
    if isEmpty:
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if distanceField == []:
                    isFree = isFreeSpace(matrix, row, col, cardRows, cardCols)
                else:
                    isFree = isFreeInField(matrix, row, col, cardRows, cardCols, distanceField)
                if isFree:
                    res.append([ row, col, 0 ] )            
                    if getComponents != None:
                        getComponents.append( {} )
        return res
   
    colorComponents = identifyCardComponents(card)                  

    posValue = {}
    for color in colorComponents:
        for pos in colorComponents[color]:
            r = floodfill(card, pos[0], pos[1])
            posValue[ (pos[0], pos[1]) ] = len(r)

    for row in range(len(matrix)):
       for col in range(len(matrix[row])): 
            key = (row, col, cardRows, cardCols)
            if key in isFreeDict:
                isFree = isFreeDict[ key ]
            else:
                if distanceField == []:
                    isFree = isFreeSpace(matrix, row, col, cardRows, cardCols)
                else:
                    isFree = isFreeInField(matrix, row, col, cardRows, cardCols, distanceField)
                isFreeDict[ key ] = isFree
                if isFree: #also set true for all smaller cards
                    for rrr in range(2, cardRows):
                        for ccc in range(2, cardCols):
                            k = (row, col, rrr, ccc )
                            isFreeDict[ k ] = True

            if isFree:        
                key = (row, col, cardRows, cardCols)
                if key in isCardInTouchDict:
                    isTouch = isCardInTouchDict[ key ]
                else:
                    isTouch = isCardTouching(matrix, row, col, card)
                    isCardInTouchDict[ key ] = isTouch
                if isTouch:
                    #compute cost of adding
                    writeCard(row, col, card, matrix)
                    colorLengths = []
                    connectedCells = {}
                    for color in colorComponents:
                        for pos in colorComponents[color]:
                            r = floodfill(matrix, row+pos[0], col+pos[1])
                            if len(r) > posValue[ (pos[0], pos[1]) ]:
                                for cell in r:
                                    if not cell in connectedCells:
                                        connectedCells[ cell ] = r[cell]
                    writeCard(row, col, card, matrix, 0)
                    costOfAdding = len(connectedCells)
                    res.append([ row, col, costOfAdding] )
                    if getComponents != None:
                        getComponents.append( connectedCells )
    return res



def drawMatrix(board, filename, _cellWidth = 60, cards = [], components = {}):
        def cell2center(cell):
            return int(cell[0]*_cellWidth + _cellWidth/2), int(cell[1]*_cellWidth + _cellWidth/2)

        numRows = len(board)
        numCols = len(board[0])
        width = _cellWidth*numCols
        height = _cellWidth*numRows
        img = Image.new('RGB',(width,height),"white")
        draw = ImageDraw.Draw(img)
        _cardOutline = "#CD853F"
        _gridColor = "#888888"
        _gridColor = "#ADACB5"
        _componentColor = "#FFFF00"
        _originColor = "#ff69b4"
        _originColor2 = "#f8c8dc"
        for row in range(len(board)):
            for col in range(len(board[row])):
                value = board[row][col]
                if value != 0:
                    draw.rectangle([col*_cellWidth, row*_cellWidth, (col+1)*_cellWidth, (row+1)*_cellWidth], fill=_colors[ value ] )
        draw.line([0,0, width,0 ], fill = "#000000", width = 3)
        draw.line([0,height, width, height ], fill = "#000000", width = 3)

        draw.line([0,0, 0,height ], fill = "#000000", width = 3)
        draw.line([width,0, width,height ], fill = "#000000", width = 3)

        for i in range(1,numRows):
            draw.line([0,i*_cellWidth, width, i*_cellWidth ], fill = _gridColor, width = 2)
        for i in range(1,numCols):
            draw.line([i*_cellWidth,0,i*_cellWidth, height ], fill = _gridColor, width = 2)
   
        cellCircles = {} 
        for cell in components:
            r1,c1 = cell2center(cell)
            r2,c2 = cell2center(components[cell])
            draw.line([c1,r1,c2,r2], fill=_componentColor, width = 1)
            cellCircles[ (r1,c1) ] = True
            cellCircles[ (r2,c2) ] = True

        eps = _cellWidth/10
        for cell in cellCircles:
            draw.ellipse([ cell[1]-eps, cell[0]-eps, cell[1]+eps, cell[0]+eps], fill=_componentColor)

        eps = _cellWidth/5
        for cardpos in cards:
            row, col, card = cardpos
            cardRows, cardCols = cardSize(card)
            x1 = col*_cellWidth
            y1 = row*_cellWidth
            x2 = (col+cardCols)*_cellWidth
            y2 = (row+cardRows)*_cellWidth
            draw.line([x1,y1,  x2,y1,  x2,y2, x1,y2, x1,y1 ], fill = _cardOutline, width = 4)
            r1,c1 = cell2center([row, col])
            draw.ellipse([ c1-eps, r1-eps, c1+eps, r1+eps ], outline = _originColor, fill=_originColor2, width = 1 )


        img.save(filename)


def png2base64(filename, width = None):
    img = Image.open(filename)
    if width != None:
        w,h = img.size
        h2 = int((width/w)*h)
        print("Resizing image from", img.size, "to", width,h2)
        img = img.resize( (width, h2) )
        print("new size", img.size)

    buff = io.BytesIO()
    img.save(buff,format="PNG")
    buff.seek(0)
    datauri = base64.b64encode(buff.read()).decode("ascii")
    return datauri, img.size[0], img.size[1]


def png2img(filename, width):
#    uri,w,h = png2base64(filename, width = width)
    uri,w,h = png2base64(filename)
    height = int((width/w)*h)
    fstr = 'width="{}" height="{}" '.format(width, height)
    res = '<img {} src="data:image/png;base64,{}"/><br>'.format(fstr,uri)
    return res


def jpg2base64(filename):
    img = Image.open(filename)
    buff = io.BytesIO()
    img.save(buff,format="JPEG")
    buff.seek(0)
    datauri = base64.b64encode(buff.read()).decode("ascii")
    return datauri, img.size[0], img.size[1]


def jpg2img(filename, width):
    uri,w,h = jpg2base64(filename)
    height = int((width/w)*h)
    fstr = 'width="{}" height="{}" '.format(width, height)
    res = '<img {} src="data:image/jpeg;base64,{}"/><br>'.format(fstr,uri)
    return res