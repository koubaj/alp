import base as BASE
import copy, random, time, sys, os
from PIL import Image, ImageDraw

# all the sizes and positions are Row and Column
class Card:
    def __init__(self, position, size, data):
        self.position = position
        self.size = size
        self.data = data
        self.colors = self.get_colors()

    def rotate_cclockwise(self):
        R, C = self.size
        new_data = []

        for col in range(C):
            temp = []
            for row in range(R):
                temp.append(self.data[row][-col -1])
            new_data.append(temp)
        self.data = new_data
        self.size = [C, R]

    # Getting the edge position of colors, to know where they are located
    def get_color_pos(self):
        R, C = self.size

        # Add key values to dictionary "positions"
        positions = {}
        for color in self.colors:
            positions[color] = []

        # Loop only around the edges
        for row in range(R):
            for col in range(C):
                if (row != 0) and (row != R - 1) and (col != 0) and (col != C - 1):
                    continue

                # Everything that is being checked here is only around the edges
                if self.data[row][col] in self.colors:
                    positions[self.data[row][col]].append([row, col])
        return positions

    # Getting colors that are on card, relative to the card
    def get_colors(self):
        R, C = self.size
        colors = []
        for r in range(R):
            for c in range(C):
                if (self.data[r][c] not in colors) and (self.data[r][c] != 0):
                    colors.append(self.data[r][c])
        colors.sort()
        return colors
    
    # Printing card data
    def __str__(self):
        R, C = self.size
        out = ""
        for r in range(R):
            for c in range(C):
                out += str(self.data[r][c]) + " "
            out += "\n"
        return out

# Probably uselless
class Board:
    

    def __init__(self, size):
        self.size = size
        self.board = self.generate_board()
        self.static_cards = []
        self.player_cards = []

    def generate_board(self):
        R, C = self.size
        board = []
        for i in range(R):
            board.append([0] * C)
        return board
    
    def measure_path(self):
        card = self.player_cards[-1]
        mr, mc = card.position
        mR, mC = card.size

        visited = []
        length_sum = 0

        # Go through all edge positions on the card and then sum all the paths that got out of the bounds of the card => they were connected to other card
        poses = card.get_color_pos()
        for color in card.colors:
            for pos in poses[color]:
                start_pos = [pos[0] + mr, pos[1] + mc]
                stack = [start_pos]
                outside_card = False
                length = 0

                while stack != []:
                    r, c = stack.pop()

                    # Algorithm already visited this position 
                    if [r, c] in visited:
                        continue

                    # The point is outside this card, which means that it is measuring
                    # newly created path
                    if (r > (mr + mR) - 1) or (c > (mc + mC) - 1) or (r < mr) or (c < mc):
                        outside_card = True

                    if r != 0 and self.board[r-1][c] == color:
                        stack.append([r-1, c])
                    if c != 0 and self.board[r][c-1] == color:
                        stack.append([r, c-1])
                    if r != self.size[0] -1 and self.board[r+1][c] == color:
                        stack.append([r+1, c])
                    if c != self.size[1] -1 and self.board[r][c+1] == color:
                        stack.append([r, c+1])

                    length += 1
                    visited.append([r,c])
                
                if not outside_card:
                    length = 0

                length_sum += length    

        return length_sum

    def insert_static_card(self, card):
        # checking if the card is not out of the game board
        if (card.position[0] + card.size[0] > self.size[0]) or (card.position[1] + card.size[1] > self.size[1]):
            return False
        
        # appending the card array
        self.static_cards.append(card)

        # adding the card on the board
        r, c = card.position
        R, C = card.size
        for row in range(R):
            for col in range(C):
                self.board[r + row][c + col] = card.data[row][col]

    def insert_player_card(self, card):
        # checking if the card is not out of the game board
        if (card.position[0] + card.size[0] > self.size[0]) or (card.position[1] + card.size[1] > self.size[1]) or (card.position[0] < 0) or (card.position[1] < 0):
            return False

        r, c = card.position
        R, C = card.size

        # checking if the card doesnt collide with any other card - it works
        for p_card in self.static_cards:
            pr, pc = p_card.position
            pR, pC = p_card.size

            if ((r + R) - 1 >= pr) and (r <= (pr + pR) - 1) and ((c + C) - 1 >= pc) and (c <= (pc - 1) + pC):    # The cards are colliding
                return False

        self.player_cards.append(card)

        for row in range(R):
            for col in range(C):
                self.board[r + row][c + col] = card.data[row][col]

        return True
    
    def remove_player_card(self, card):
        # Remove the card from list
        self.player_cards.remove(card)

        # Fill board with 0 on the place of the card
        r, c = card.position
        R, C = card.size
        for row in range(R):
            for col in range(C):
                self.board[r + row][c + col] = 0

    # printing the board
    def __str__(self):
        R, C = self.size
        out = ""
        for r in range(R):
            for c in range(C):
                out += str(self.board[r][c]) + " "
            out += "\n"
        return out

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

unconnectable = [ [0,3,0],
                  [3,3,0],
                  [3,0,0],
                  [3,3,3]]

class Player(BASE.BasePlayer):
    def __init__(self, login, boardRows, boardCols, cardsAtHand):
        super().__init__(login, boardRows, boardCols, cardsAtHand)
        self.playerName = "Stream of Consciousness"

        # Setting up board
        self.game_board = Board([self.boardRows, self.boardCols])

        # Setting up cards
        #random.shuffle(self.cardsAtHand)
        #random.seed()
        self.myCards = []
        self.placedCards = []
        for card in self.cardsAtHand:
            self.myCards.append(Card(None, [len(card), len(card[0])], card))

    def play(self,newCardOnDesk):
        if len(newCardOnDesk) == 3:
            card = Card([newCardOnDesk[0], newCardOnDesk[1]], [len(newCardOnDesk[2]), len(newCardOnDesk[2][0])], newCardOnDesk[2])
            self.cardsOnDesk += [newCardOnDesk]
            self.placedCards.append(card)
            self.game_board.insert_static_card(card)

        if len(self.cardsAtHand) == 0:
            return []

        def return_Data(index, ret_card):
            # Remove my card
            self.cardsAtHand = self.cardsAtHand[:index] + self.cardsAtHand[index+1:]
            self.myCards = self.myCards[:index] + self.myCards[index+1:]

            # Inserting card on the board
            self.game_board.insert_static_card(ret_card)
            self.placedCards.append(ret_card)
            r, c = ret_card.position
            data = ret_card.data

            self.cardsOnDesk += [[r,c,data]]
            return [r,c,data]

        # First move, no cards are placed yet
        if len(self.cardsOnDesk) == 0:
            cardindx = random.randint(0, len(self.cardsAtHand)-1)  #random index of a card
            card = self.cardsAtHand[cardindx]
            cardRows = len(card)
            cardCols = len(card[0])
            row = random.randint(0, self.boardRows-cardRows-1) 
            col = random.randint(0, self.boardCols-cardCols-1)

            placing_card = Card([row, col], [cardRows, cardCols], card)
            return_Data(cardindx, placing_card)

            return [row, col, card ]   

        # Loading placed and playable cards
        longest_len = 0
        temp_card = None
        cardindx = None

        # Looping through my cards
        for index, card in enumerate(self.myCards):
            for i in range(4):  # Rotating the card to check all the variations
                #print(card)
                # Lgic for finding the best place for that card
                R, C = card.size
                card_poses = card.get_color_pos()

                # Looping through all placed cards edge color positions, wich are on my playable card
                for key, value in card_poses.items():
                    # look for the same keys in the placed cards
                    for placed_card in self.placedCards:
                        placed_c_c_pos = placed_card.get_color_pos()
                        if key not in placed_c_c_pos:
                            continue

                        placed_poses = placed_c_c_pos[key]
                        # Now that I know the pos of the colors, try to put the card there
                        for p_pos in placed_poses:
                            pR, pC = placed_card.size
                            pr, pc = placed_card.position

                            # Also loop through all of my card positions which can be connected
                            for my_pos in value:
                                placed = False
                                if (p_pos[0] == 0) and (my_pos[0] == R - 1): # On the top, also checks if my card can be connected from the bottom
                                    # Calculate the card position to actually connect those colors
                                    card.position = [pr - R, pc + p_pos[1] - my_pos[1]]
                                    #print("from top", card.position)
                                    placed = self.game_board.insert_player_card(card)

                                elif (p_pos[0] == pR - 1) and (my_pos[0] == 0): # On the bottom, and card on the top
                                    # Calculate the card position to actually connect those colors
                                    card.position = [pr + pR, pc + p_pos[1] - my_pos[1]]
                                    #print("from bottom:", card.position)
                                    placed = self.game_board.insert_player_card(card)

                                elif (p_pos[1] == 0) and (my_pos[1] == C - 1): # On the left, and card on the right   
                                    # Calculate the card position to actually connect those colors
                                    card.position = [pr + p_pos[0] - my_pos[0], pc - C]
                                    #print("from left:", card.position)
                                    placed = self.game_board.insert_player_card(card)

                                elif (p_pos[1] == pC - 1) and (my_pos[1] == 0): # On the right, and card on the left
                                    # Calculate the card position to actually connect those colors
                                    card.position = [pr + p_pos[0] - my_pos[0], pc + pC]
                                    #print("from right:", card.position)
                                    placed = self.game_board.insert_player_card(card)

                                # Measure the longest path
                                if placed:
                                    length = self.game_board.measure_path()
                                    #print(length)
                                    #print(game_board)
                                    if length > longest_len:
                                        longest_len = length
                                        temp_card = copy.deepcopy(card)
                                        cardindx = index
                                    self.game_board.remove_player_card(card)
                                    #print(game_board)
                                
                # rotate the card
                card.rotate_cclockwise()

        if longest_len == 0:
            # Then just slap any card somewhere if possible
            # Looping through my cards
            for index, card in enumerate(self.myCards):
                sides = 1
                if card.size[0] != card.size[1]:
                    sides = 2
                
                for i in range(sides):  # Rotating the card to check all the variations
                    R, C = card.size

                    for placed_card in self.placedCards:
                        pR, pC = placed_card.size
                        pr, pc = placed_card.position

                        # Try placing card around the placed card
                        # Generating all positions where the card could theoretically be placed
                        poses = []
                        for col in range(pc - (C - 1), pc + pC):
                            poses.append([pr - R, col])
                            poses.append([pr + pR, col])
                        for row in range(pr - (R - 1), pr + pR):
                            poses.append([row, pc - C])
                            poses.append([row, pc + pC])

                        # placing it there
                        for pos in poses: 
                            card.position = pos
                            if self.game_board.insert_player_card(card):
                                self.game_board.remove_player_card(card)
                                temp_card = copy.deepcopy(card)
                                return return_Data(index, temp_card)

                    card.rotate_cclockwise()

            # No cards found
            return []
                        
        else:
            #print(longest_len)
            #print(temp_card.position)
            #print(temp_card)
            #print(self.game_board)
            return return_Data(cardindx, temp_card)

if __name__ == "__main__":
    tmp = [C44a, C44b, C33a,C33c, C53c, C53b, unconnectable]*1

    p1 = Player("testA", 17, 25, tmp)
    p2 = Player("testB", 17, 25, tmp)

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