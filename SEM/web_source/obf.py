import re, glob, os, sys, string, random

if len(sys.argv) != 2:
    print("usage", sys.argv[0], " <active 0/1>")
    quit()

isActive = int(sys.argv[1])


funs = {}
for fn in files:
    with open(fn,"rt") as f:
        for line in f:
            if line.find("def") == 0:
                res = re.search("def (\w*)\(.*\):", line)
#                print("L", line.strip(), res)
                if res and len(res.groups()) > 0:
                    fname = res.group(1)
#                    print(line, fname)
                    funs[ fname ] = 1

s = list(funs.keys())
s.sort()
#print(s)

funs = ['gameOfTwo', 'card2line', 'card2matrixString', 'card2png', 'cardSize', 'changeColor', 'checkOutput', 'checkTypes', 'drawMatrix', 'floodfill', 'getAllPlacements', 'getPlayerVersion', 'geta', 'getfn', 'handler', 'identifyCardComponents', 'inBoard', 'isCardTouching', 'isEmptyMatrix', 'isFreeInField', 'isFreeSpace', 'items2table', 'makeTest', 'png2base64', 'png2img', 'printBoard', 'printCard', 'printStatus', 'removeSecret', 'replaceBrackets', 'rfn', 'rotateCard', 'test1', 'toColor', 'toGreen', 'toName', 'toRed', 'value2str', 'writeCard', 'writeHTML', 'writePts', 'oneMove', 'showValidMode', 'showInvalidMove']

if isActive != 1:
    quit()


def randomfn():
    rl = random.randint(3,10)
    return ''.join( [ random.choice(string.ascii_letters) for _ in range(rl) ] )

codes2fn = {}
fun2code = {}
for function in funs:
    while True:
        code = randomfn()
        if not code in codes2fn:
            codes2fn[ code ] = function
            fun2code[ function ] = code
            break
print("Codes", fun2code)



for fn in files:
    f = open(fn,"rt")
    lines = f.readlines()
    f.close()
    f = open(fn,"wt")
    cnt = 0
    for line in lines:
        for function in funs:
            if line.find(function) >= 0:
                new = line.replace(function, fun2code[ function ] )
#                print(fn, ": replacing", line.strip(), "by", new.strip())
                line = new
                cnt += 1
        f.write(line)
    print("File", fn, " replaced", cnt)
    f.close()