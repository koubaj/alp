import base as BASE
import copy, random, time, sys, os
from PIL import Image, ImageDraw


#basic cards with colors 1 and 2
#note that Brute can provide you also other cards!
C44a = [ [0,1,2,0], 
         [1,1,2,2],
         [2,2,1,1],
         [0,2,1,0] ]  

C44b = [ [0,0,1,0], 
         [1,1,1,0],
         [0,2,2,2],
         [0,2,0,0] ] 

C53b = [ [0,1,0], 
         [0,1,0],
         [0,1,0],
         [0,1,1],
         [0,0,0] ]

C53c = [ [0,1,0], 
         [0,1,0],
         [0,1,1],
         [0,2,2],
         [0,2,0] ]

C33a = [ [0,1,0], 
         [1,1,2],
         [0,0,2] ]

C33c = [ [1,2,1], 
         [2,2,2], 
         [1,2,1] ]


class Player(BASE.BasePlayer):
    def __init__(self, login, boardRows, boardCols, cardsAtHand):
        super().__init__(login, boardRows, boardCols, cardsAtHand)
        self.playerName = "My awesome player"

    def play(self,newCardOnDesk):
        """ this method is called during the game. 
            The input argument newCardOnDesk is:
            - [] if other player didn't place any card in his move), or
            - [row, col, cardMatrix], which informs your player that cardMatrix was placed at row,col to the game board
            
            Return value: 
            - [ row, col, cardMatrix ] if you want to place a card, or
            - [] if no card can be placed 
        """

        #recommened steps 
        #step 0: write newCardOnDesk to list of cards that are on the board game
        #step 1: compute all possible placement of your all (so for available) cards
        #step 2: evaluate each placement, i.e., compute score for it
        #step 3: select card that you want to place to the game board, mark it as used (not available in future)
        #step 4: return your placement, or [] if no placement can be made
        #the following code DOES NOT provides correct moves, 
        #it just return random card at random position

        if len(newCardOnDesk) == 3:
            self.cardsOnDesk += [ newCardOnDesk ]

        if len(self.cardsAtHand) == 0:
            return []

        cardindx = random.randint(0, len(self.cardsAtHand)-1)  #random index of a card
        card = self.cardsAtHand[cardindx]
        cardRows = len(card)
        cardCols = len(card[0])
        row = random.randint(0, self.boardRows-cardRows-1) 
        col = random.randint(0, self.boardCols-cardCols-1)
        self.cardsAtHand = self.cardsAtHand[:cardindx] + self.cardsAtHand[cardindx+1:]  #remove selected card so its not used in future
        self.cardsOnDesk += [ [row, col, card ] ]
        return [row, col, card ]


if __name__ == "__main__":
    """ when you run:
        python3 player.py

        you should get set of .png files with the progress of the game
    """

    tmp = [C44a, C44b, C33a,C33c, C53c, C53b]*1

    p1 = Player("testA", 19, 23, tmp)
    p2 = Player("testB", 19, 23, tmp)

    p2move = []
    gameStep = 0
    while True:
        p1move = p1.play(p2move)
        print("p1 returned", p1move)
        p1.drawCards(p1.boardRows, p1.boardCols, p1.cardsOnDesk,"move-{:02}b-A.png".format(gameStep))

        p2move = p2.play(p1move)    
        print("p2 returned", p2move)
        p2.drawCards(p2.boardRows, p2.boardCols, p2.cardsOnDesk,"move-{:02}b-B.png".format(gameStep))
        gameStep += 1
        if p1move == [] and p2move == []:
            print("end of game")
            quit()


