import base as BASE
import copy, random, time, sys, os
from PIL import Image, ImageDraw
def DebugPrint(grid):
    key = {-1:chr(11035), 0:chr(11036), 1:chr(128997), 2:chr(128999), 3:chr(129000), 4:chr(129001), 5:chr(129002), 6:chr(129003), 7:chr(128992), 8:chr(128993), 9:chr(128994), 10:chr(128995), 11:chr(128996)}
    for line in grid:
        for cell in line:
            print(key[cell], end="")
        print()
    print()
def try_fill_in_easy(x,y,karta,pole):
    vyska = len(karta)
    sirka = len(karta[0])
    for h in range(x,x+vyska):
        for k in range(y,y+sirka):
            if pole[h][k] != -1:
                return False
    if (x-1) > -1:
        tmp_x = x - 1
        for slouec in range(y,y+sirka):
            if pole[tmp_x][slouec] != -1:
                return True
    if (y-1) > -1:
        tmp_y = y - 1
        for radek in range(x,x+vyska):
            if pole[radek][tmp_y] != -1:
                return True
            
    if (x+vyska) < len(pole):
        tmp_x = x+vyska
        for sloupec in range(y,y+sirka):
            if pole[tmp_x][sloupec] != -1:
                return True
    
    if (y+sirka)<len(pole[0]):
        tmp_y = y + sirka
        for radek in range(x,x+vyska):
            if pole[radek][tmp_y] != -1:
                return True
    return False
                
def find_me_place_easy(karta,pole:list):
    #pole = do_2D_copy(hraci_pole)
    '''
    Vstup = 2D pole karty a 2D hraci pole
    Vystup = nejlepsi mozna zahratelna pozice
    '''
    #karta = do_2D_copy(origo_karta)
    for radky in range((len(pole)-len(karta)+1)):
        for sloupce in range((len(pole[0])-len(karta[0])+1)):
            if pole[radky][sloupce] == -1:
                fill_in = try_fill_in_easy(radky,sloupce,karta,pole)
                if fill_in:
                    return 0,radky,sloupce
    return -1,-1,-1


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

def vytvor_hraci_pole(radky,sloupce):
    '''
    Na vstupu dostane pole se dvema prvky a vrati 2D pole tvorene -1 o danem rozmeru
    '''   
    hraci_pole = []
    for i in range(radky):
        hraci_pole.append([-1]*sloupce)
    return hraci_pole

def rotate_card(pole:list):
    '''
    Vstup = 2D pole ktere chceme zrotovat
    Vystup = zrotovane 2D pole
    '''
    kopie = []
    for wtf in range(len(pole)):
        kopie.append(pole[wtf][:])
    rotace = []
    for i in range(len(kopie[0])):
        b = []
        for j in range(len(kopie)-1,-1,-1):
            b.append(kopie[j][i])
        rotace.append(b)
    return rotace

def karty_v_ruce(pole):
        karty_ruka = []
        for karta in pole:
            karty_ruka.append(karta)
            for j in range(3):
                rotace = rotate_card(karta)
                karty_ruka.append(rotace)
                karta = rotace
        return karty_ruka

def obsah_karet(pole):
        max_vyska = 0
        max_sirka = 0
        for karta in pole:
            vyska = len(karta)
            sirka = len(karta[0])
            if vyska > max_vyska:
                max_vyska = vyska
            if sirka > max_sirka:
                max_sirka = sirka
        return max_vyska,max_sirka

def try_fill_in(x,y,karta,pole):
    vyska = len(karta)
    sirka = len(karta[0])
    for h in range(x,x+vyska):
        for k in range(y,y+sirka):
            if pole[h][k] != -1:
                return False
    smery = ((1,0),(-1,0),(0,1),(0,-1))
    for smer in smery:
        if (smer[0] == -1) or (smer[1] == -1):
            if ((y+smer[1]) < 0) or ((x+smer[0]) < 0):
                    continue
            if smer[1] == -1:
                for rakdy_leva in range(x,x+vyska):
                    if pole[rakdy_leva][y-1] != -1:
                        return True
            else:
                for sloupce_nad in range(y,y+sirka):
                    if pole[x-1][sloupce_nad] != -1:
                        return True
                
        else:
            if ((y+sirka-1+smer[1]) == len(pole[0])) or ((x+vyska-1+smer[0]) == len(pole)):
                continue
            if smer[1] == 1:
                for rakdy_prava in range(x,x+vyska):
                    if pole[rakdy_prava][y+sirka] != -1:
                        return True
            else:
                for sloupce_pod in range(y,y+sirka):
                    if pole[x+vyska][sloupce_pod] != -1:
                        return True
    return False

def get_points(x,y,karta,pole):
    hraci_pole = copy.deepcopy(pole)
    
    opakovani = 0
    for i in range(x,(x + len(karta))):
        hraci_pole[i][y:(y + len(karta[0]))] = karta[opakovani]
        opakovani += 1
    
    jsem_v_karte = []
    for a in range(x,x + len(karta)):
        for b in range(y,y + len(karta[0])):
            jsem_v_karte.append([a,b])

    body = 0
    nechod = []
    magazine = []
    for radky in range(x,x+len(karta)):
        for sloupce in range(y,y + len(karta[0])):
            used = []
            if ([radky,sloupce] not in nechod) and (hraci_pole[radky][sloupce] != 0):
                used.append([radky,sloupce])
            else:
                continue
            barva = hraci_pole[radky][sloupce]
            magazine.append([radky,sloupce])
            smery = [(1,0),(-1,0),(0,1),(0,-1)]
            while len(magazine)!= 0:
                if magazine[0] not in used:
                    used.append(magazine[0])
                for i in smery:
                    if (i[0] == -1) or (i[1] == -1):
                        if (magazine[0][0] + i[0] < 0) or (magazine[0][1] + i[1] < 0):
                            continue
                        else:
                            if i[0] == -1:
                                if hraci_pole[magazine[0][0] + i[0]][magazine[0][1]] == barva:
                                    a = [magazine[0][0]+i[0],magazine[0][1]]
                                    if a not in used:
                                        magazine.append(a)
                            else:
                                if hraci_pole[magazine[0][0]][magazine[0][1]+i[1]] == barva:
                                    a = [magazine[0][0],magazine[0][1]+i[1]]
                                    if a not in used:
                                        magazine.append(a)
                    else:
                        if (magazine[0][0] + i[0] >= len(pole)) or (magazine[0][1] + i[1] >= len(pole[0])):
                            continue
                        else:
                            if i[0] == 1:
                                if hraci_pole[magazine[0][0] + i[0]][magazine[0][1]] == barva:
                                    a = [magazine[0][0]+i[0],magazine[0][1]]
                                    if a not in used:
                                        magazine.append(a)
                            else:
                                if hraci_pole[magazine[0][0]][magazine[0][1]+i[1]] == barva:
                                    a = [magazine[0][0],magazine[0][1]+i[1]]
                                    if a not in used:
                                        magazine.append(a)
                magazine.pop(0)

            nice = False
            for q in used:
                if not q in jsem_v_karte:
                    nice = True
                nechod.append(q)
            if nice:
                body += len(used)
            else:
                continue
    return body
                
def find_me_place(koukni,origo_karta:list,pole:list):
    #pole = do_2D_copy(hraci_pole)
    '''
    Vstup = 2D pole karty a 2D hraci pole
    Vystup = nejlepsi mozna zahratelna pozice
    '''
    #karta = do_2D_copy(origo_karta)
    karta = origo_karta
    # if koukni[0] - len(karta) < 0:
    #     zacni0 = 0
    # else:
    #     zacni0 = koukni[0] - len(karta)
    # if koukni[1] - len(karta[0]) < 0:
    #     zacni1 = 0
    # else:
    #     zacni1 = koukni[1] - len(karta[0])
    # if koukni[2] + len(karta) > len(pole):
    #     zacni2 = len(pole) - len(karta)
    # else:
    #     zacni2 = koukni[2] + len(karta)
    # if koukni[3] + len(karta[0]) > len(pole[0]):
    #     zacni3 = len(pole[0]) - len(karta[0])
    # else:
    #     zacni3 = koukni[3] + len(karta[0])
    nejvetsi = -1
    for radky in range((len(pole)-len(karta)+1)):
        for sloupce in range((len(pole[0])-len(karta[0])+1)):
    # for radky in range(zacni0,zacni2):
    #     for sloupce in range(zacni1,zacni3):
            if pole[radky][sloupce] == -1:
                fill_in = try_fill_in(radky,sloupce,karta,pole)
                if fill_in:
                    bodiky = get_points(radky,sloupce,karta,pole)
                    if bodiky > nejvetsi:
                        nejvetsi = bodiky
                        f_karta = origo_karta
                        f_radek = radky
                        f_sloupec = sloupce
                        f_bodiky = nejvetsi
                else:
                    continue
    if nejvetsi == -1:
        return -1,-1,-1,-1
    else:
        return f_bodiky,f_radek,f_sloupec,f_karta
    
def poloz_kartu(radek,sloupec,karta,pole):
    opakovani = 0
    for i in range(radek,(radek + len(karta))):
        pole[i][sloupec:(sloupec + len(karta[0]))] = karta[opakovani]
        opakovani += 1
    
class Player(BASE.BasePlayer):
    
    def __init__(self, login, boardRows, boardCols, cardsAtHand):
        super().__init__(login, boardRows, boardCols, cardsAtHand)
        self.playerName = "D0MDi"
        self.cardsAtHand = karty_v_ruce(self.cardsAtHand)
        self.kouknout = [0,0,boardRows - 1,boardCols-1]
        self.pouzite = []
        # self.min_radek = 0
        # self.max_radek = boardRows - 1
        # self.min_sloupec = 0
        # self.max_sloupec = boardCols - 1
        self.hraci_pole = vytvor_hraci_pole(boardRows,boardCols)

    
    def play(self,newCardOnDesk):
        """ this method is called during the game. 
            The input argument newCardOnDesk is:
            - [] if other player didn't place any card in his move), or
            - [row, col, cardMatrix], which informs your player that cardMatrix was placed at row,col to the game board
            
            Return value: 
            - [ row, col, cardMatrix ] if you want to place a card, or
            - [] if no card can be placed 
        """
        # DebugPrint(self.hraci_pole)
        # if self.tournament:
        #         if len(self.cardsOnDesk) == 0 and newCardOnDesk == []:
        #             cardindx = random.randint(0, len(self.cardsAtHand)-1)  #random index of a card
        #             card = self.cardsAtHand[cardindx]
        #             cardRows = len(card)
        #             cardCols = len(card[0])
        #             row = random.randint(0, self.boardRows-cardRows-1) 
        #             col = random.randint(0, self.boardCols-cardCols-1)
        #             for i in range(4):
        #                 odebrani = (4*(cardindx//4)) + i
        #                 self.cardsAtHand.pop(odebrani)
        #             #remove selected card so its not used in future
        #             self.cardsOnDesk += [ [row, col, card ] ]
        #             self.kouknout = [row,col,row + len(card),col + len(card[0])]
        #             poloz_kartu(row,col,card,self.hraci_pole)
        #             # self.min_radek = row
        #             # self.min_sloupec = col
        #             # self.max_radek = row + len(card)
        #             # self.max_sloupec = col + len(card[0])
        #             return [row, col, card ]
        #         else:
        #             if newCardOnDesk == []:
        #                 pass
        #             else:
        #                 poloz_kartu(newCardOnDesk[0],newCardOnDesk[1],newCardOnDesk[2],self.hraci_pole)
        #                 if newCardOnDesk[0] < self.kouknout[0]:
        #                     self.kouknout[0] = newCardOnDesk[0]
        #                 if newCardOnDesk[1] < self.kouknout[1]:
        #                     self.kouknout[1] = newCardOnDesk[1]
        #                 if newCardOnDesk[0]+len(newCardOnDesk[2]) > self.kouknout[2]:
        #                     self.kouknout[2] = newCardOnDesk[0]+len(newCardOnDesk[2])
        #                 if newCardOnDesk[1]+len(newCardOnDesk[2][0]) > self.kouknout[3]:
        #                     self.kouknout[3] = newCardOnDesk[1]+len(newCardOnDesk[2][0])
        #             if len(self.cardsAtHand) == 0:
        #                 return []
        #             else:
        #                 for i in range(len(self.cardsAtHand)):
        #                     karta = self.cardsAtHand[i]
        #                     d_body,row,col,card = find_me_place(self.kouknout,karta,self.hraci_pole)
        #                     index = i
        #                     if d_body >= 0:
        #                         odebrani = (4*(index//4))
        #                         for j in range(4):
        #                             odebrani = odebrani + j
        #                             print(len(self.cardsAtHand))
        #                             print(odebrani)
        #                             self.cardsAtHand.pop(odebrani)
        #                         #remove selected card so its not used in future
        #                         self.cardsOnDesk += [ [row, col, card ] ]
        #                         self.kouknout = [row,col,row + len(card),col + len(card[0])]
        #                         poloz_kartu(row,col,card,self.hraci_pole)
        #                         return [row,col,card]
        #                 return []
        # else:
            
        


        if len(self.cardsOnDesk) == 0 and newCardOnDesk == []:
            card = self.cardsAtHand[0]
            row = self.boardRows//2 
            col = self.boardCols//2
            index = 0
            for i in range(4):
                odebrani = index + i
                self.pouzite.append(odebrani)
            self.cardsOnDesk += [ [row, col, card ] ]
            poloz_kartu(row,col,card,self.hraci_pole)
            return [ row,col,card ]
        else:
            if newCardOnDesk != []:
                poloz_kartu(newCardOnDesk[0],newCardOnDesk[1],newCardOnDesk[2],self.hraci_pole)
            for index in range(len(self.cardsAtHand)):
                if index in self.pouzite:
                    continue
                karta = self.cardsAtHand[index]
                d_body,d_radek,d_sloupec = find_me_place_easy(karta,self.hraci_pole)
                d_index = 4*(index//4)
                if d_body > -1:
                    for i in range(4):
                        odebrani = d_index + i
                        self.pouzite.append(odebrani)
                    poloz_kartu(d_radek,d_sloupec,karta,self.hraci_pole)
                    self.cardsOnDesk += [[d_radek,d_sloupec,karta]]
                    return[ d_radek,d_sloupec,karta]
            return []





                

    
    


        #recommened steps 
        #step 0: write newCardOnDesk to list of cards that are on the board game
        #step 1: compute all possible placement of your all (so for available) cards
        #step 2: evaluate each placement, i.e., compute score for it
        #step 3: select card that you want to place to the game board, mark it as used (not available in future)
        #step 4: return your placement, or [] if no placement can be made
        #the following code DOES NOT provides correct moves, 
        #it just return random card at random position

        # if len(newCardOnDesk) == 3:
        #     self.cardsOnDesk += [ newCardOnDesk ]

        # if len(self.cardsAtHand) == 0:
        #     return []

        # cardindx = random.randint(0, len(self.cardsAtHand)-1)  #random index of a card
        # card = self.cardsAtHand[cardindx]
        # cardRows = len(card)
        # cardCols = len(card[0])
        # row = random.randint(0, self.boardRows-cardRows-1) 
        # col = random.randint(0, self.boardCols-cardCols-1)
        # self.cardsAtHand = self.cardsAtHand[:cardindx] + self.cardsAtHand[cardindx+1:]  #remove selected card so its not used in future
        # self.cardsOnDesk += [ [row, col, card ] ]
        # return [row, col, card ]


# if __name__ == "__main__":
#     """ when you run:
#         python3 player.py

#         you should get set of .png files with the progress of the game
#     """

#     tmp = [C44a, C44b, C33a, C33c, C53c, C53b]*1

#     p1 = Player("testA", 19, 23, tmp)
#     p2 = Player("testB", 19, 23, tmp)

#     p2move = []
#     gameStep = 0
#     while True:
#         p1move = p1.play(p2move)
#         print("p1 returned", p1move)
#         p1.drawCards(p1.boardRows, p1.boardCols, p1.cardsOnDesk,"move-{:02}b-A.png".format(gameStep))
#         p2move = p2.play(p1move)    
#         print("p2 returned", p2move)
#         p2.drawCards(p2.boardRows, p2.boardCols, p2.cardsOnDesk,"move-{:02}b-B.png".format(gameStep))
#         if p1move == [] and p2move == []:
#             print("end of game")
#             quit()
#         gameStep += 1