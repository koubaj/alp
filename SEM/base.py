
# base class for Player, do not change this file !!!!
# this file will be replaced by Brute/Tournament anyway, so your changes will not be reflected
# if you want to work with some instance variables (self.xyz etc), define them in your Player in player.py file


#import PIL for drawing to PNG files
from PIL import Image, ImageDraw

class BasePlayer:
    
    def __init__(self, login, boardRows, boardCols, cardsAtHand):
        """Constructor for the base class. 
            login .. string representing user name/login (it will be given by Brute)
            boardRows  .. int, number of rows in the game board (desk)
            boardCols .. int, number of columns in the game board (desk)
            cardsAtHand .. is list [ card1, card2, ... ]
                where card_i is 2D matrix describing the card
        """                
        self.userLogin = login
        self.boardRows = boardRows
        self.boardCols = boardCols
        self.cardsOnDesk = []
        self.cardsAtHand = cardsAtHand
        self.tournament = False
        self.playerName = "my great player"
        self.timeout = 1  #timeout in seconds for constructor and play()

        # just for drawing
        self._colors = {}
        self._colors[0] = "#ffffff"
        self._colors[1] = "#636940"
        self._colors[2] = "#59A96A"
        self._colors[3] = "#ffdd4a"
        self._colors[4] = "#fe9000"
        self._colors[-2] = "#a3d9ff"
        self._colors[-1] = "#cccccc" #sunglow

    def play(self, newCardOnDesk):
        """This function is the only one that will be called directly by Brute. Write your implementation inside player.py file
        """
        pass

    def drawCards(self, numRows, numCols, cards, filename, _cellWidth = 60):

        """Debugging function, you can draw your cards in PNG file with it. Look at player.py for example
        """

        def getCenter(row, col):
            return row*_cellWidth + _cellWidth/2, col*_cellWidth + _cellWidth/2

        _cardOutline = "#CD853F"
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
                    draw.rectangle([cellCol*_cellWidth, cellRow*_cellWidth, (cellCol+1)*_cellWidth, (cellRow+1)*_cellWidth], fill=self._colors[ value ] )
            eps = _cellWidth/6
            rc,cc = getCenter(row, col)                    
            draw.ellipse([cc-eps,rc-eps,cc+eps,rc+eps], fill=_originColor2)

        for i in range(1,numRows):
            draw.line([0,i*_cellWidth, width, i*_cellWidth ], fill = _gridColor, width = 2)
        for i in range(1,numCols):
            draw.line([i*_cellWidth,0,i*_cellWidth, height ], fill = _gridColor, width = 2)
        eps = 2
        draw.line([eps,eps,width-eps,eps,width-eps,height-eps,eps, height-eps, eps, eps], fill=_gridColor, width=5)    
        img.save(filename)


