import base, random, copy, re


#supporting tools for gemblo, most for printing to html/javascript

canvasid = 0

__all__=[]

def __dir__():
    return []


def replaceBrackets(text):
    t1 = text.replace("<", "<")
    t2 = t1.replace(">", ">")
    return t2;

def pre(text):
    return "<pre>{}</pre>\n".format(text)

def pre2(text):
    return "<code>{}</code>\n".format(replaceBrackets(text))


def removeSecret(text):
    a = text.split("\n");
    res = "";
    for line in a:
            line = line.replace("player","player");
            line = line.replace("player","player");
            line = line.replace("player","player");
player.py"):
                pos = line.find("/player.py")
                line = line[pos+1:]
                
            res += line + "\n";
    return res;

#print traceback
def pt(msg):
    a = removeSecret(msg)
    b = replaceBrackets(a);
    return pre(b);


def avg(array):
    s = 0;
    if (len(array) == 0):
        return -1;
    for i in array:
        s += i;
    return 1.0*s / len(array)


def getPlayerVersion(player):
    s = player.algorithmName;
    so = "";
    for c in s:
        if (c.isalnum()):
            so += c;
    return so;

def toColor(text, color):
    return "<font color=\"{}\">{}</font>".format(color,text)

def toRed(text):
    return toColor(text, "#FF0000");

def toGreen(text):
    return toColor(text, "#00bc10");

def shuffle(array):
    for i in range(len(array)-1):
        j = random.randint(i+1, len(array)-1);
        array[i], array[j] = array[j], array[i]


def toName(i):
    if i == 1:
        return "red";
    return "green"


def printBoard(board, label=True, R = 18):
    """ returns an output string to draw the board. assuming that board() and cell() functions are defined somewhere in html.
        board is drawn to canvas of given id
    """
    global canvasid
    canvasid += 1

    size = 0
    pq = "[ ";
    first = True
    for p in board:
        for q in board[p]:
            if abs(p) > size:
                size = abs(p)
            if abs(q) > size:
                size = abs(q)

            value = board[p][q]
            if first == False:
                pq += ",";
            pq += "[{},{},{}]".format(p,q,value);  
            first = False
    pq += "]";

    width = R*2.2*size
    height = R*2*size

    width = int(R*(3**0.5))*size + 3*R
    height = 2*R*size*0.9

    out = ""

    out += "<canvas id=\"{}\" width=\"{}\" height=\"{}\" style=\"border:1px solid #aaaaaa;\">Your browser does not support HTML5 canvas </canvas>\n".format(canvasid,width, height);


    
    out += "<script>\n";
    out += "var b=" + pq + ";\n";
    if label:
        out += "board({},b,1,{});\n".format(canvasid,R);
    else:
        out += "board({},b,0,{});\n".format(canvasid,R);
    out += "</script>\n"; 
    return out


def items2table(numCols, items):
    res = "<table>"
    idx = 0
    row = ""
    for i in range(len(items)):
        if idx % numCols == 0:
            if row != "":
                row += "</tr>"
                res += row
            row = "<tr>"
        row += "<td>" + items[i] + "</td>\n"
        idx += 1

    row += "</tr>"

    res += row
    res += "</table>\n";
    return res