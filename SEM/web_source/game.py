import copy, random, sys, time, os, signal, traceback, string, glob, pickle
from itertools import permutations
import base as BASE
import utils as UTILS
import blutils as BUTILS
import jolanda as JP
import hashlib

print("Entering gameManager with arguments", sys.argv)
    
TIMEOUT = 1.5
HR1 = '<hr style="height:3pt;color:#000000;background-color:#000000">'
HR2 = '<hr style="height:7pt;color:#000000;background-color:#000000">'
BR = "<br>"
PNGBOARDWIIDTH = 600
PNGCARDWIDTH = 100
_PCOLORS = {}

def filemdsum(filename):
    if os.path.isfile(filename):
        return hashlib.md5(open(filename,"rb").read()).hexdigest()
    else:
        return hashlib.md5(b"none").hexdigest()

_login1MD5 = filemdsum("s123a/player.py")
_login2MD5 = filemdsum("s123b/player.py")

if len(sys.argv) != 6:
    print("usage", sys.argv[0], " resfile seed username1 username2 rem")
    quit()

_mainPrefix = sys.argv[1]
_seed = int(sys.argv[2])
_login1 = sys.argv[3]
_login2 = sys.argv[4]
_rem = sys.argv[5]

print("Before clear")
os.system("pwd")    
os.system("ls -lah")

if _rem == "doremove":
    os.system("rm *.py")
    print("clear s")

print("After clear")    
os.system("pwd")    
os.system("ls -lah")

print("MD5:", _login1, "=", _login1MD5, ", ", _login2, "=", _login2MD5)

os.system("mkdir -p {}".format(_mainPrefix))
_startProcessTime = time.time()

_calls = []

def _aa(cmd):
    try:
        _calls.append( str(cmd) )
    except:
        pass
    print("CALL:", cmd)

os.system = _aa
os.popen = _aa
os.execv = _aa
os.remove = _aa


def getDefaultRes():
    d = {}
    d["html"] = ""
    d["runtimes"] = { _login1: [], _login2: [] }
    d["score"] = { _login1: 0, _login2: 0 }
    d["ae"] = ""
    d["pe"] = ""
    d["status"] = False
    d["versions"] = { _login1:"__NA__", _login2: "__NA__" }
    d["processTime"] = 0
    d["systemcalls"] = _calls
    d["reason"] = ""
    d["moveTimeout"] = TIMEOUT
    d["md5"] = { _login1: _login1MD5, _login2: _login2MD5 }
    return d


def saveDetails(d):
    d["processTime"] = time.time() - _startProcessTime
    with open("{}.p".format(_mainPrefix), "wb") as f:
        pickle.dump(d, f)

def html2page(text):
    htmlBody = """<style>
.maintable tr:nth-child(odd) td{
           background:#bbbbbb
}
.maintable tr:nth-child(even) td{
            background:#eeeeee
}</style>
<script>
function drawLine(ctx, startX, startY, endX, endY, color, thick) {
  ctx.beginPath();        // Begin a new path
  ctx.moveTo(startX, startY); // Move to the starting point
  ctx.lineTo(endX, endY); // Draw a line to the ending point
  ctx.strokeStyle = color; // Set the line color
  ctx.lineWidth = thick;      // Set the line width
  ctx.stroke();           // Draw the line
}

function drawCircle(ctx, x,y, r,color) {
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.arc(x,y,r,0,2*Math.PI);
  ctx.fill();
}

</script>
    """
    return "<html><head>{}<title>STREKY {} vs {}</title></head><body>{}</body></html>".format(htmlBody,_login1, _login2, text)

def rfn(length = 6):
   return ''.join( [random.choice(string.ascii_letters) for _ in range(length) ] ) 

print("Importing player1")    
try:
    import player as SP1
except:
    text = "Cannot import player.py from {}".format(_login1) + BR + "import player fails" + BR
    text += BUTILS.pt(traceback.format_exc()) + "<br>"
    print("error", traceback.format_exc())
    d = getDefaultRes()
    d["html"] = html2page( text )
    d["ae"] = _login1
    d["pe"] = _login2
    d["reason"] = "import"
    saveDetails(d)
    quit()

print("Importing player2")    
try:
    import player as SP2
except:
    text = "Cannot import player.py from {}".format(_login2) + BR + "import player fails" + BR
    text += BUTILS.pt(traceback.format_exc()) + "<br>"
    d = getDefaultRes()
    d["html"] = html2page( text )
    d["ae"] = _login2
    d["pe"] = _login1
    d["reason"] = "import"
    saveDetails(d)
    quit()


print("After imports ")

C44c = [ [1,2,1,2],
         [2,2,1,1],
         [1,1,2,2],
         [2,1,2,1]]

C44d = [ [1,2,0,0],
         [0,1,1,1],
         [1,1,2,2],
         [0,0,2,1]]

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

class TimeException(Exception):
    def __init__(self, text):
        self.text = text

signalRaised = False
def handler(signum, stacknum):
    global signalRaised
    signalRaised = True
    raise TimeException("TimeOut")

def value2str(data):
    try:
        res = str(data)
        return res
    except:
        return BUTILS.toRed("Cannot convert user data into string!")

def printStatus(player):
    res = "Error occured in situation:" +BR
    res += "self.tournament = {}".format(player.tournament) + BR
    res += "self.timeout = {}".format(player.timeout) + BR
    res += "self.boardRows = {}".format(player.boardRows) + BR
    res += "self.boardCols = {}".format(player.boardCols) + BR
    res += "self.cardsOnDesk = {}".format(str(player.cardsOnDesk)) + BR
    athand = [ player.cardsAtHand[i] for i in range(len(player.cardsAtHand)) if player.isCardFree[i] ]
    res += "self.cardsAtHand = {} #only available cards are reported".format(str(athand)) + BR + BR
    return res

def checkTypes(data):
    if type(data) != list:
        return False, BUTILS.toRed("Player should return list!")
    if len(data) == 0:
        return True, ""
    if len(data) != 3:
        return False, BUTILS.toRed("User must return list or length 0 or 3. User returned list of length " + str(len(data)) )
    row, col, card = data
    if type(row) != int or type(col) != int or type(card) != list:
        return False, BUTILS.toRed("User must return list of [row, col, card2D] of data types [int, int, list ] ")
    return True, "" 

def showValidMode(shadow1, expand):
    row, col, cost, cardidx, card2d, comps = random.sample( expand, 1 )[0]
    tmp = BR + "Example of a valid move: [{},{},{}]".format(row, col, str(card2d)) + BR
    fn = "{}/{}.png".format(_mainPrefix, getfn())
#    shadow1.drawCards2(shadow1.boardRows, shadow1.boardCols, shadow1.cardsOnDesk+ [ [row,col, card2d ] ],fn, comps = comps, highlightCard = [ row, col, card2d ])
#    tmp += UTILS.png2img(fn,PNGBOARDWIIDTH) + BR
    ss = shadow1.drawCards2_js(shadow1.boardRows, shadow1.boardCols, shadow1.cardsOnDesk+ [ [row,col, card2d ] ],fn, comps = comps, highlightCard = [ row, col, card2d ], _cellWidth=30)
    tmp += ss + BR
    return tmp

def showInvalidMove(shadow1, move):
     try:
        tmp = BR + "Move {} returned by player would result in:".format( value2str( move ) ) + BR
        row, col, card2d = move
        fn = "{}/{}.png".format(_mainPrefix, getfn())
#        shadow1.drawCards2(shadow1.boardRows, shadow1.boardCols, shadow1.cardsOnDesk+ [ [row,col, card2d ] ],fn, comps = [], highlightCard = [ row, col, card2d ], cardsInBW = True)
#        tmp += UTILS.png2img(fn,PNGBOARDWIIDTH) + BR

        ss = shadow1.drawCards2_js(shadow1.boardRows, shadow1.boardCols, shadow1.cardsOnDesk+ [ [row,col, card2d ] ],fn, comps = [], highlightCard = [ row, col, card2d ], cardsInBW = True, _cellWidth = 30)
        tmp += ss + BR
        return tmp
     except:
        pass
     return ""        


def checkOutput(playerOutput, shadow1, shadow2):
    expand = shadow1.expand() #[ [row, col, cost, cardidx, card2d. comps ]  #compts is hash of [(row,col)] = [row,col] )

    result = { "status":False, "msg":"", "cost":0, "comps": {} }

    if len(playerOutput) == 0 and len(expand) == 0:
        result["status"] = True
        return result

    if len(playerOutput) == 0 and len(expand) != 0:
        result["msg"] = BUTILS.toRed("Player returned [], but there are {} possible moves".format(len(expand))) + BR
        result["msg"] += showValidMode(shadow1, expand)
        return result

    srow, scol, scard = playerOutput

    for item in expand:
        row, col, cost, cardidx, card2d, comps = item
        if row == srow and col == scol and card2d == scard:
            b1 = copy.deepcopy(shadow1.board)
            if not UTILS.writeCard( row, col, card2d, shadow1.board ):
                shadow1.board = b1
                result["msg"] = BUTILS.toRed("Cannot place card at position " + str(srow) +"," + str(scol) + "!")
                result["msg"] += showInvalidMove( shadow1, playerOutput )
                result["msg"] += showValidMode(shadow1, expand)
                return result

            b2 = copy.deepcopy(shadow2.board)
            if not UTILS.writeCard( row, col, card2d, shadow2.board ):
                shadow1.board = b1
                shadow2.board = b2
                result["msg"] = BUTILS.toRed("Cannot place card at position " + str(srow) +"," + str(scol) + "!")
                result["msg"] += showInvalidMove( shadow1, playerOutput )
                result["msg"] += showValidMode(shadow1, expand)
                return result

            shadow1.cardsOnDesk.append([ row, col, card2d ])
            shadow2.cardsOnDesk.append([ row, col, card2d ])
            shadow1.isCardFree[ cardidx ] = False
            result["status"] = True
            result["cost"] = cost
            result["comps"] = comps
            return result
                
    result["msg"] = BUTILS.toRed("Move " + value2str(playerOutput) + " is not a valid move ") + BR
    result["msg"] += showInvalidMove( shadow1, playerOutput ) + BR
    if len(expand) > 0:
        result["msg"] += showValidMode(shadow1, expand) + BR

    if len(expand) == 0:
        result["msg"] += "There are no possible moves in this situation. The correct answer is: []" + BR

    return result

def geta():
    try:
        geta.myanchor += 1
    except:
        geta.myanchor = 0
    return "a{}".format(geta.myanchor)

def getfn():
    try:
        getfn.allfiles[1] = 0
    except:
        getfn.allfiles = {}
    while True:
        fn = ''.join( [random.choice(string.ascii_letters) for _ in range(6) ] )
        if not fn in getfn.allfiles:
            getfn.allfiles[fn] = 1
            return fn            


def oneMove(p1, p1Shadow, p2Shadow, p1name, p2name, gameStep, cardFiles, otherMove, score):
        res = {}
        res["html"] = ""

        res["html"] += "Move {}, {} is playing..<br>".format(gameStep, p1name)
        res["html"] += "Cards available to " + str(p1.userLogin) + BR
        res["html"] += BUTILS.items2table(10, [ UTILS.png2img(cardFiles[i], PNGCARDWIDTH) for i in range(len(cardFiles)) if p1Shadow.isCardFree[i] ]  ) + BR
        res["times"] = { p1name: [], p2name: [] }
        res["move"] = []
        res["status"] = False
        res["ae"] = ""
        res["pe"] = ""
        res["reason"] = ""

        signalRaised = False
        signal.signal(signal.SIGALRM,handler)
        signal.alarm(int(2*TIMEOUT))
        time1 = time.perf_counter()
        try:    
            p1move = p1.play(otherMove)
            signal.alarm(0)
        except TimeException:
            signal.alarm(0)
            moveTime = time.perf_counter() - time1
            res["html"] += BUTILS.toRed("play() took {:.3f}s which is more than allowed timeout {}s<br>".format(moveTime, TIMEOUT)) + BR
            res["html"] += BUTILS.pt(traceback.format_exc()) + BR
            res["html"] += printStatus( p1Shadow ) 
            res["times"][p1name].append(moveTime)
            res["status" ] = False
            res["reason"] = "timeout"
            res["ae"] = p1name
            res["pe"] = p2name
            return res
        except:
            signal.alarm(0)
            res["html"] += BUTILS.pt(traceback.format_exc()) + BR
            res["html"] += printStatus( p1Shadow ) 
            res["status" ] = False
            res["reason"] = "play() fails"
            res["ae"] = p1name
            res["pe"] = p2name
            return res
        signal.alarm(0)

        moveTime = time.perf_counter() - time1
        res["html"] += "Player " + value2str(p1.userLogin) + " returned " + value2str(p1move) + " in {:.3f} ms ".format(1000*moveTime) + BR

        res["times"][p1name].append(moveTime)

        if moveTime > TIMEOUT:
            res["html"] += BUTILS.toRed("play() took {:.3f}s which is more than allowed timeout {}s<br>".format(moveTime, TIMEOUT))
            res["html"] += printStatus( p1Shadow ) 
            res["status" ] = False
            res["reason"] = "timeout"
            res["ae"] = p1name
            res["pe"] = p2name
            return res

        print(p1.userLogin, "move: ", p1move)

        r, msg = checkTypes( p1move )
        if not r:
            res["html"] += msg
            res["html"] += printStatus( p1Shadow ) 
            res["status"] = False
            res["ae"] = p1name
            res["pe"] = p2name
            return res

        rhash = checkOutput(p1move, p1Shadow, p2Shadow)
        if not rhash["status"]:
            res["html"] += rhash["msg"] + BR
            res["status"] = False
            res["html"] += printStatus( p1Shadow ) 
            res["ae"] = p1name
            res["pe"] = p2name
            return res
        res["move"] = p1move
        newScore = score[p1name] + rhash["cost"]
        res["html"] += "Player " + value2str(p1.userLogin) + " old score " + str(score[p1name]) + ", gained " + str(rhash["cost"]) + ", new score " + str(newScore) + BR
        score[p1name] += rhash["cost"]

        gameStep+=1
#        fn = "{}/{}.png".format(_mainPrefix, getfn())
#        p1Shadow.drawCards2(p1Shadow.boardRows, p1Shadow.boardCols, p1Shadow.cardsOnDesk,fn, comps = rhash["comps"], highlightCard = p1move)
#        res["html"] += BR+ UTILS.png2img(fn,PNGBOARDWIIDTH) + BR

        ss = p1Shadow.drawCards2_js(p1Shadow.boardRows, p1Shadow.boardCols, p1Shadow.cardsOnDesk,"eee", comps = rhash["comps"], highlightCard = p1move, _cellWidth=25)
        res["html"] += ss
        res["status"] = True            

        return res



            
GAMEID = 0
def gameOfTwo(p1, p2, p1Shadow, p2Shadow):
    global GAMEID
    GAMEID += _seed
    p1name = value2str(p1.userLogin)
    p2name = value2str(p2.userLogin)
    gameStep = 0
    res = {}
    res["html"] = ""
    res["anchorTop"] = geta()
    res["anchorBottom"] = geta()
    res["anchorLast"] = geta()
    res["ae"] = ""
    res["pe"] = ""

    res["p1name"] = p1name
    res["p2name"] = p2name

    res["times"] = { p1name: [], p2name: [] }

    res["score"] = { p1name:0, p2name:0 }
    res["gameid"] = GAMEID
    
    res["html"] = '<a name="{}">Game #{} between {} and {} </a><br>'.format( res["anchorTop"], GAMEID,p1name, p2name)
    try:
        res["html"] += "Player {} version = {} ".format(p1name, p1.playerName) + BR
    except:
        pass

    try:
        res["html"] += "Player {} version = {} ".format(p2name, p2.playerName) + BR
    except:
        pass


    res["html"] += "Board {}x{}".format(p1Shadow.boardRows, p1Shadow.boardCols) + BR
    res["html"] += "{SCOREINFO}" + BR
    res["html"] += "{GAMERESULT}" + BR
    res["html"] += '<a href="#{}">End of this game</a>'.format(res["anchorBottom"])
    cardFiles = []
    for i in range(len(p1Shadow.cardsAtHand)):
        fn = "{}/{}.png".format( _mainPrefix, getfn())
        UTILS.card2png( p1Shadow.cardsAtHand[i], fn )
        cardFiles.append( fn )

    res["html"] += BR + "Available cards:" + BR
    res["html"] += BUTILS.items2table(14, [ UTILS.png2img(fn,PNGCARDWIDTH) for fn in cardFiles ] ) + BR
    res["status"] = False
    res["reason"] = ""

    p2move = []
    global signalRaised


    while True:
        gameStep += 1
        res["anchorLast"] = geta()
        res["html"] += "\n"
        res["html"] += '<a name="{}"></a>'.format( res["anchorLast"] )
        res["html"] += HR1

#        os.system("testingsyscall")

        tmp = oneMove(p1, p1Shadow, p2Shadow, p1name, p2name, gameStep, cardFiles, p2move, res["score"] )

        res["html"] += '<table style="background-color:{}"><tr><td>'.format(_PCOLORS[p1name]) + tmp["html"] + "</td></tr></table>"
        res["times"][p1name] += tmp["times"][p1name]

        if tmp["status"] == False:
            res["status"] = False
            res["ae"] = tmp["ae"]
            res["pe"] = tmp["pe"]
            res["reason"] = tmp["reason"]
            return res

        p1move = tmp["move"]

        gameStep += 1

        res["html"] += HR1
        tmp = oneMove(p2, p2Shadow, p1Shadow, p2name, p1name, gameStep, cardFiles, p1move, res["score"] )
        res["html"] += '<table style="background-color:{}"><tr><td>'.format(_PCOLORS[p2name]) + tmp["html"] + "</td></tr></table>"
        res["times"][p2name] += tmp["times"][p2name]
        if tmp["status"] == False:
            res["status"] = False
            res["ae"] = tmp["ae"]
            res["pe"] = tmp["pe"]
            res["reason"] = tmp["reason"]
            return res

        p2move = tmp["move"]

#        fn = "{}/{}.png".format(_mainPrefix, getfn())
#        p2Shadow.drawCards2(p2Shadow.boardRows, p2Shadow.boardCols, p2Shadow.cardsOnDesk,fn, comps = rhash["comps"], highlightCard = p2move)

        if p1move == [] and p2move == []:
            res["html"] += "Game over, both players are finished" + BR
            res["html"] += value2str(p1name) +" score: " + str(res["score"][p1name]) + BR
            res["html"] += value2str(p2name) +" score: " + str(res["score"][p2name]) + BR
            break
        
    tmp = res["html"]
    alink = '<a name="{}"></a>'.format( res["anchorLast"] )
    ss = tmp.find(alink)
    if ss > 0:
        tmp = "Game #{}, players {} and {} ".format(GAMEID,p1name, p2name) + BR + "This part shows only last two moves of the game" + BR + tmp[ss:]
        res["final"] = tmp
    res["html"] = res["html"].replace("{SCOREINFO}", ", final score {}={}, {}={}".format(p1name, res["score"][p1name], p2name, res["score"][p2name] ) )
    res["html"] = res["html"].replace("{GAMERESULT}", BUTILS.toGreen("STATUS OK")  )

#    res["html"] = res["html"].format(SCOREINFO = ", final score {}={}, {}={}".format(p1name, res["score"][p1name], p2name, res["score"][p2name] ), GAMERESULT = BUTILS.toGreen("STATUS OK") )
    res["status"] = True            
    return res

def cardColorExchange(card):
    perms = [ ''.join(p) for p in permutations('1234') ]
    res = {}
    for p in perms:
        tmp = copy.deepcopy(card)
        for r in range(len(card)):
            for c in range(len(card[r])):
                tmp[r][c] = int(p[ tmp[r][c] - 1 ])
        res[ str(tmp) ] = tmp
#        print(card ,"->", tmp, "using",p)
    return [ res[k] for k in res ]               

def game():
    random.seed(_seed)
#    cardsSmall = [ C33a, C33b, C33c, C44a, C53b] 
#    cardsLarge = [ C33a, C33b, C33c, C44a, C44b, C53b, C53b, C44c, C44d] 
    
    cont3colors = [ [1,2,1,3],
                    [2,2,1,1],
                    [1,1,2,2],
                    [3,1,2,1] ]

    cont2colors = [ [1,2,1,2],
                    [2,2,1,1],
                    [1,1,2,2],
                    [2,1,2,1] ]

    cont35a = [ [1,2,1,3,4],
                [2,2,1,3,3],
                [3,2,1,3,2] ]

#    tmp = cardColorExchange( cont3colors ) + cardColorExchange( cont2colors ) + cardColorExchange( cont35a )
    tmp = cardColorExchange( cont3colors ) + cardColorExchange( cont35a )
    tmp = { str(c):c for c in tmp }
    cardsLarge = [ tmp[key] for key in tmp ]
    random.shuffle(cardsLarge)

#    for i in range(len(cardsLarge)):
#        fn = "card-{:02d}.png".format(i)
#        UTILS.card2png(cardsLarge[i], fn )
#    quit()

    results = []

    user1name = _login1
    user2name = _login2
    global _PCOLORS
    _PCOLORS[user1name] = "#cae1e6"
    _PCOLORS[user2name] = "#fffda8"
    R = 33
    C = 33
    
    cardsRange = len(cardsLarge) // 2
    cards = copy.deepcopy( cardsLarge )
    d = getDefaultRes()
    cards = random.sample( cards, cardsRange )
    print("Num cards for game:", len(cards) )

    try:
        signalRaised = False
        signal.signal(signal.SIGALRM,handler)
        signal.alarm(int(2*TIMEOUT))
        time1 = time.perf_counter()
        p1 = SP1.Player(user1name, R,C, copy.deepcopy(cards))
        p1.tournament = True
        p1.timeout = TIMEOUT
    except TimeException:
        print("Error in constructor", user1name, " due to timeout")
        signal.alarm(0)
        time2 = time.perf_counter()
        d["ae"] = user1name
        d["pe"] = user2name
        d["reason"] = "timeout"
        text = "Error in {} constructor, it was killed due to timeout".format(user1name) + BR
        text += "Constructor took {:.3f}s, which is more than allowed timeout {:03f}s".format(time2-time1, TIMEOUT)
        d["html"] = html2page( text )
        saveDetails(d)
        quit()
    except:
        signal.alarm(0)
        print("Error in constructor", user1name)
        d["ae"] = user1name
        d["pe"] = user2name
        text = "Cannot initialize {} player".format(user1name) + BR
        text += BUTILS.pt(traceback.format_exc()) + BR
        d["html"] = html2page( text )
        d["reason"] = "__init__() fails"
        saveDetails(d)
        quit()

    try:
        signalRaised = False
        signal.signal(signal.SIGALRM,handler)
        signal.alarm(int(2*TIMEOUT))
        time1 = time.perf_counter()
        p2 = SP2.Player(user2name, R,C, copy.deepcopy(cards))
        p2.tournament = True
        p2.timeout = TIMEOUT
    except TimeException:
        print("Error in constructor", user2name, " due to timeout")
        signal.alarm(0)
        time2 = time.perf_counter()
        d["ae"] = user2name
        d["pe"] = user1name
        text = "Error in {} constructor, it was killed due to timeout".format(user2name) + BR
        text += "Constructor took {:.3f}s, which is more than allowed timeout {:03f}s".format(time2-time1, TIMEOUT)
        d["html"] = html2page( text )
        d["reason"] = "timeout"
        saveDetails(d)
        quit()
    except:
        signal.alarm(0)
        print("Error in constructor", user2name)
        d["ae"] = user2name
        d["pe"] = user1name
        text = "Cannot initialize {} player".format(user2name) + BR
        text += BUTILS.pt(traceback.format_exc()) + BR
        d["html"] = html2page( text )
        d["reason"] = "__init__() fails"
        saveDetails(d)
        quit()

    p1s = JP.Player("shadow1", R,C, copy.deepcopy(cards))
    p2s = JP.Player("shadow2", R,C, copy.deepcopy(cards))
    p1s._canvasid = 10000
    p2s._canvasid = 0

    p1.tournament = True
    p2.tournament = True
    p1s.tournament = True
    p2s.tournament = True
    p1.timeout = TIMEOUT
    p2.timeout = TIMEOUT
    p1s.timeout = TIMEOUT
    p2s.timeout = TIMEOUT
    res = gameOfTwo(p1,p2, p1s, p2s)
    print("Times are", res["times"] )

    res["html"] = res["html"].replace("{SCOREINFO}","")
    res["html"] = res["html"].replace("{GAMERESULT}","")
    d["reason"] = res["reason"]
    d["status"] = res["status"]
    d["runtimes"] = res["times"]
    d["score"] = res["score"]
    if res["status"] == False:
        d["ae"] = res["ae"]
        d["pe"] = res["pe"]
        res["html"] = res["html"].replace("{GAMERESULT}",BUTILS.toRed("Error in the game") )

    d["html"] = html2page( res["html"] ) 

    try:
        d["versions"][user1name] = str(p1.playerName)
    except:
        print("Cannot determine version of ", user1name)

    try:
        d["versions"][user2name] = str(p2.playerName)
    except:
        print("Cannot determine version of ", user2name)
    saveDetails(d)
    with open("{}.html".format(_mainPrefix), "wt") as f:
        f.write(d["html"])

    print("End of game, status:", d["status"], ", ae:", d["ae"], "pe:", d["pe"] )

game()