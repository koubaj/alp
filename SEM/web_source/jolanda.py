import base as BASE
import utils as UTILS
import copy, random
from PIL import Image, ImageDraw

def __dir__():
    return []

__all__=[]    

C44a = [ [0,1,2,0], 
         [1,1,2,2],
         [2,2,1,1],
         [0,2,1,0] ]  #2 L-cesty dlouhe

C44b = [ [0,0,1,0], 
         [1,1,1,0],
         [0,2,2,2],
         [0,2,0,0] ]  #4 L cesty kratke

C53b = [ [0,1,0], [0,1,0],[0,1,0],[0,1,1],[0,0,0] ]
C53c = [ [0,1,0], [0,1,0],[0,1,1],[0,2,2],[0,2,0] ]

C33a = [ [0,1,0], [1,1,2],[0,0,2] ]
C33b = [ [0,2,0], [0,2,0], [0,2,0] ]
C33c = [ [1,2,1], [2,2,2], [1,2,1] ]


class Player(BASE.BasePlayer):
    def __init__(self, login, boardRows, boardCols, cardsAtHand):
        super().__init__(login, boardRows, boardCols, cardsAtHand)
        self.board = [ [0]*self.boardCols for _ in range(self.boardRows) ]
        self.isCardFree = [ True ]*len(self.cardsAtHand)
        self.playerName = "BrutePlayer1"
        self.distanceField = copy.deepcopy( self.board )
        self._canvasid = 0

    def updateDistanceField(self):
        for row in range(self.boardRows):

            for i in range(self.boardCols):
                self.distanceField[row][i] = 0

            col = self.boardCols-1
            while col >= 0:
                while col >= 0 and self.board[row][col] != 0:
                    col-=1
                if col < 0:
                    break
                i = 1
                while col >=0 and self.board[row][col] == 0:
                    self.distanceField[row][col] = i
                    i += 1
                    col -= 1


    def expand(self):
        allExpands = [] #each one is [row, col, cost, cardindex, card2D ] 
        isFreeDict = {}
        isCardInTouchDict = {}
        resultCache = {}
        self.updateDistanceField()

#        print("Board")
#        UTILS.printCard(self.board)
#        print("DF")
#        UTILS.printCard(self.distanceField)    

        for cardi in range(len(self.cardsAtHand)):
            if not self.isCardFree[cardi]:
                continue
            card = self.cardsAtHand[cardi]
            for _ in range(4):
                card = UTILS.rotateCard(card)
                if not str(card) in resultCache:
                    comps = []
                    allpositions = UTILS.getAllPlacements(self.board, card, getComponents = comps, isFreeDict = isFreeDict, isCardInTouchDict = isCardInTouchDict, distanceField = self.distanceField)
                    resultCache[ str(card) ] = [ [allpositions[i][0], allpositions[i][1], allpositions[i][2], cardi, card, comps[i] ] for i in range(len(allpositions)) ]
                allExpands +=  resultCache[ str(card) ] 
        return allExpands                
 
    def play(self,newCardOnDesk):
        #card is "[ row, col, card2D ] or []
        #print(self.userLogin, "writing", newCardOnDesk, " on my desk")
        if len(newCardOnDesk) != 0:
            self.cardsOnDesk.append( newCardOnDesk )
            UTILS.writeCard( newCardOnDesk[0], newCardOnDesk[1], newCardOnDesk[2], self.board )
    
        allExpands = self.expand()

        if len(allExpands) == 0:
            return []                
        maxCost = max( [ pos[2] for pos in allExpands ] )
        bestPositions = [ pos for pos in allExpands if pos[2] == maxCost ]
        cardsizes = [ len(pos[4])*len(pos[4][0]) for pos in bestPositions ]
        maxCardSize = max(cardsizes)
        bestPositions = [ pos for pos in bestPositions if len(pos[4])*len(pos[4][0]) == maxCardSize ]

        randomPlacement = random.sample(bestPositions, 1)[0]
                        
        row, col, cost, cardindex, card2d, _ = randomPlacement
        self.cardsOnDesk.append( [ row, col, card2d ] )
        self.isCardFree[ cardindex ] = False
        UTILS.writeCard( row, col, card2d, self.board )  
        return [ row, col, card2d ]


    def drawCards2(self, numRows, numCols, cards, filename, _cellWidth = 60, comps = {}, highlightCard = [], cardsInBW = False):
        """Debugging function, you can draw your cards in PNG file with it. Look at player.py for example
        """
        def getCenter(row, col):
            return row*_cellWidth + _cellWidth/2, col*_cellWidth + _cellWidth/2
        def bw(color):
            r = color.replace("#","")[0:2]            
            g = color.replace("#","")[2:4]            
            b = color.replace("#","")[4:]
            r = int(r,16)
            g = int(g,16)
            b = int(b,16)
            v = (r+g+b)//3
            v = hex(v).replace("0x","")
            v = "#{}{}{}".format(v,v,v)
            return v

        _cardOutline = "#CD853F"
        _cardOutlineHL = "#FFFF10"
        _gridColor = "#888888"
        _gridColor = "#ADACB5"
        _componentColor = "#FFFF00"
        _originColor = "#ff69b4"
        _originColor2 = "#f8c8dc"

        width = _cellWidth*numCols
        height = _cellWidth*numRows
        img = Image.new('RGBA',(width,height),"white")
        draw = ImageDraw.Draw(img)

        for card in cards:
            row, col, matrix = card
            cardRows = len(matrix)
            cardCols = len(matrix[0])
            eps = 3
            draw.rectangle([col*_cellWidth-eps, row*_cellWidth-eps, (col+cardCols)*_cellWidth+eps, (row+cardRows)*_cellWidth+eps], outline = _cardOutline, fill=(0,0,0,0), width=10)
            for r in range(cardRows):
                for c in range(cardCols):
                    cellRow = r + row
                    cellCol = c + col
                    value = matrix[r][c]
                    if value == 0:
                        value = -1
                    color = self._colors[ value ]
                    if cardsInBW and card != highlightCard:
                        color = bw(color) 
                    draw.rectangle([cellCol*_cellWidth, cellRow*_cellWidth, (cellCol+1)*_cellWidth, (cellRow+1)*_cellWidth], fill=color )
            eps = _cellWidth/6
            rc,cc = getCenter(row, col)                    
            draw.ellipse([cc-eps,rc-eps,cc+eps,rc+eps], fill=_originColor2)

        if len(highlightCard) == 3:
            row, col, card = highlightCard
            cardRows = len(card)
            cardCols = len(card[0])                    
            eps = 3
            pts = [ [0,0],[1,0],[1,1],[0,1],[0,0] ]
            pts = [ ( (col+p[0]*cardCols)*_cellWidth, (row+p[1]*cardRows)*_cellWidth) for p in pts ]
            draw.line(pts, fill=_cardOutlineHL, width=10)

        for cell in comps:
            eps = _cellWidth/10
            y1,x1 = getCenter(cell[0], cell[1])
            y2,x2 = getCenter(comps[cell][0], comps[cell][1])
            draw.line([x1,y1,x2,y2], fill=_componentColor, width=2)
            draw.ellipse([x1-eps,y1-eps,x1+eps,y1+eps], fill=_componentColor, width=2)
            draw.ellipse([x2-eps,y2-eps,x2+eps,y2+eps], fill=_componentColor, width=2)

        for i in range(1,numRows):
            draw.line([0,i*_cellWidth, width, i*_cellWidth ], fill = _gridColor, width = 2)
        for i in range(1,numCols):
            draw.line([i*_cellWidth,0,i*_cellWidth, height ], fill = _gridColor, width = 2)
        eps = 2
        draw.line([eps,eps,width-eps,eps,width-eps,height-eps,eps, height-eps, eps, eps], fill=_gridColor, width=5)    
        if "jpg" in filename:
            img = img.convert('RGB')                
        img.save(filename)

    def drawCards2_js(self, numRows, numCols, cards, filename, _cellWidth = 60, comps = {}, highlightCard = [], cardsInBW = False):
        
        def getCenter(row, col):
            return row*_cellWidth + _cellWidth/2, col*_cellWidth + _cellWidth/2
        def bw(color):
            r = color.replace("#","")[0:2]            
            g = color.replace("#","")[2:4]            
            b = color.replace("#","")[4:]
            r = int(r,16)
            g = int(g,16)
            b = int(b,16)
            v = (r+g+b)//3
            v = hex(v).replace("0x","")
            v = "#{}{}{}".format(v,v,v)
            return v
        def rectLines(x,y,width, height,color, thickness = 1):            
            pts = [ [0,0],[1,0],[1,1],[0,1],[0,0] ]
            pts = [  (x+width*p[0], y+height*p[1]) for p in pts ]
            res = ""
            for pi in range(len(pts)-1):
                res += "drawLine(ctx,{},{},{},{},\"{}\", {});\n".format(pts[pi][0], pts[pi][1], pts[pi+1][0], pts[pi+1][1], color, thickness)
            return res

        _cardOutline = "#CD853F"
        _cardOutline = "#0000aa"
        _cardOutlineHL = "#FFFF10"
        _cardOutlineHL = "#FF69b4"
        _gridColor = "#888888"
        _gridColor = "#ADACB5"
        _componentColor = "#FFFF00"
        _originColor = "#ff69b4"
        _originColor2 = "#f8c8dc"
        
        width = _cellWidth*numCols
        height = _cellWidth*numRows
#        img = Image.new('RGBA',(width,height),"white")
#        draw = ImageDraw.Draw(img)

        self._canvasid += 1
        out = "\n\n"
        out += "<canvas id=\"cnv{}\" width=\"{}\" height=\"{}\" style=\"border:1px solid #aaaaaa;\">Your browser does not support HTML5 canvas </canvas>\n".format(self._canvasid,width, height);
        out += "<script>"
        out += "function drawCanvas{}(name)".format(self._canvasid) + "{\n"
        out += "let canvas = document.getElementById(name);\n".format(self._canvasid)
        out += "let ctx = canvas.getContext('2d');\n"


        for card in cards:
            row, col, matrix = card
            cardRows = len(matrix)
            cardCols = len(matrix[0])
            eps = 3
#            draw.rectangle([col*_cellWidth-eps, row*_cellWidth-eps, (col+cardCols)*_cellWidth+eps, (row+cardRows)*_cellWidth+eps], outline = _cardOutline, fill=(0,0,0,0), width=10)
            rx = col*_cellWidth-eps
            ry = row*_cellWidth-eps
            wx = cardCols*_cellWidth
            wy = cardRows*_cellWidth
#            out += "ctx.lineWidth=10;\n";
#            out += "ctx.strokeStyle = '{}';\n".format(_cardOutline)
#            out += "ctx.strokeRect({},{},{},{});\n".format(rx,ry,wx,wy)
#            out += "ctx.lineWidth=1;\n";
            for r in range(cardRows):
                for c in range(cardCols):
                    cellRow = r + row
                    cellCol = c + col
                    value = matrix[r][c]
                    if value == 0:
                        value = -1
                    color = self._colors[ value ]
                    if cardsInBW and card != highlightCard:
                        color = bw(color) 
#                    draw.rectangle([cellCol*_cellWidth, cellRow*_cellWidth, (cellCol+1)*_cellWidth, (cellRow+1)*_cellWidth], fill=color )
                    rx = cellCol*_cellWidth
                    ry = cellRow*_cellWidth
                    wx = 1*_cellWidth
                    wy = 1*_cellWidth
                    out += "ctx.fillStyle='{}';\n".format(color)
                    out += "ctx.fillRect({},{},{},{});\n".format(rx,ry,wx,wy)
            eps = _cellWidth/6
            rc,cc = getCenter(row, col)                    
            out += "//origin\n"
            out += "drawCircle(ctx,{},{},{},\"{}\");\n".format(cc,rc,_cellWidth/6,_originColor2)
#            out += "ctx.beginPath();\n"
#            out += "ctx.fillStyle = '{}';\n".format(_originColor2)
#            out += "ctx.arc({},{},{},0,Math.PI*2);\n".format(cc,rc,_cellWidth/6)
#            out += "ctx.fill();\n"
#            draw.ellipse([cc-eps,rc-eps,cc+eps,rc+eps], fill=_originColor2)

        if len(highlightCard) == 3:
            row, col, card = highlightCard
            cardRows = len(card)
            cardCols = len(card[0])                    
            eps = 3
            pts = [ [0,0],[1,0],[1,1],[0,1],[0,0] ]
            pts = [ ( (col+p[0]*cardCols)*_cellWidth, (row+p[1]*cardRows)*_cellWidth) for p in pts ]
#            draw.line(pts, fill=_cardOutlineHL, width=10)
            out += "//HL card\n"
            out += rectLines(col*_cellWidth,row*_cellWidth, cardCols*_cellWidth, cardRows*_cellWidth, _cardOutlineHL, 5)
            out += "// end of HL\n";
#            for i in range(len(pts)-1):
#                out += "ctx.lineWidth = 3;\n";
#                out += "drawLine(ctx,{},{},{},{},\"{}\");\n".format(pts[i][0],pts[i][1], pts[i+1][0],pts[i+1][1], _cardOutlineHL)
#                out += "ctx.lineWidth = 1;\n";

           
        for cell in comps:
            eps = _cellWidth/10
            y1,x1 = getCenter(cell[0], cell[1])
            y2,x2 = getCenter(comps[cell][0], comps[cell][1])
#            draw.line([x1,y1,x2,y2], fill=_componentColor, width=2)
            out += "drawLine(ctx,{},{},{},{},\"{}\",1);\n".format(x1,y1,x2,y2, _componentColor)

            out += "// comps\n";
#            draw.ellipse([x1-eps,y1-eps,x1+eps,y1+eps], fill=_componentColor, width=2)
            out += "drawCircle(ctx, {},{}, {}, \"{}\");\n".format(x1,y1,_cellWidth/10,_componentColor)
#            draw.ellipse([x2-eps,y2-eps,x2+eps,y2+eps], fill=_componentColor, width=2)
            out += "drawCircle(ctx, {},{}, {}, \"{}\");\n".format(x2,y2,_cellWidth/10,_componentColor)
        
        for i in range(1,numRows):
#            draw.line([0,i*_cellWidth, width, i*_cellWidth ], fill = _gridColor, width = 2)
            out += "drawLine(ctx, {},{},{},{},\"{}\",1);\n".format(0,i*_cellWidth, width, i*_cellWidth, _gridColor)

        for i in range(1,numCols):
#            draw.line([i*_cellWidth,0,i*_cellWidth, height ], fill = _gridColor, width = 2)
            out += "drawLine(ctx, {},{},{},{},\"{}\",1);\n".format(i*_cellWidth,0, i*_cellWidth, height, _gridColor)
        out += "//card outlines\n"

        for card in cards:
            row, col, matrix = card
            cardRows = len(matrix)
            cardCols = len(matrix[0])
            rx = col*_cellWidth
            ry = row*_cellWidth
            wx = cardCols*_cellWidth
            wy = cardRows*_cellWidth
            out += rectLines(rx,ry, wx,wy, _cardOutline, 2)


        eps = 2
#        draw.line([eps,eps,width-eps,eps,width-eps,height-eps,eps, height-eps, eps, eps], fill=_gridColor, width=5)    
        _blackColor = "#000000"
        out += "drawLine(ctx,0,0,0,{}, \"{}\",6);\n".format(height, _blackColor)
        out += "drawLine(ctx,0,{},{},{},\"{}\",6);\n".format(height,width,height, _blackColor)
        out += "drawLine(ctx,{},{},{},0,\"{}\",6);\n".format(width,height,width, _blackColor)
        out += "drawLine(ctx,{},0,0,0,\"{}\",6);\n".format(width, _blackColor)
 
        out += "}\n\n"
        out += "drawCanvas{}(\"cnv{}\");\n".format(self._canvasid, self._canvasid)
        out += "</script>"
        return out




if __name__ == "__main__":
    tmp = [C44a, C44b, C33a,C33b, C33c]*1

    p1 = Player("testA", 19,23, tmp)
    p2 = Player("testB", 19, 23, tmp)

    p2move = []
    gameStep = 0
    while True:
        p1move = p1.play(p2move)
        print("p1 returned", p1move)
        p1.drawCards(p1.boardRows, p1.boardCols, p1.cardsOnDesk,"move-{:02}b-A.png".format(gameStep))

        p2move = p2.play(p1move)    
        print("p2 returned", p2move)
        # UTILS.drawMatrix(p2.board, "move-{:02}-B.png".format(gameStep))
        p2.drawCards(p2.boardRows, p2.boardCols, p2.cardsOnDesk,"move-{:02}b-B.png".format(gameStep))
        gameStep += 1
        if p1move == [] and p2move == []:
            print("end of game")
            quit()