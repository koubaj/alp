#!/usr/bin/env python3
import glob, re, pickle, os, zlib


linesCount = {}

try:
    with open("linesCount.pickle", "rb") as f:
        linesCount = pickle.load(f)
except:
    print("Cannot load linesCount.pickle")
    print("Run ./countLines.py before sending SEM.tgz to src/")
    print("See ./countLines.py how to do it ")
#    quit()


for name in linesCount:
    print(name, " has ", linesCount[name] )


print("Loaded ", len(linesCount), " LOC infos ")

allGames = {}

versions = {}

totalOrigSize = 0
totalCompressedSize = 0

expectedGames = 10  #each allGames[ user1 ] [ user 2] should has this amount of records

allDirs = glob.glob("runs/*/*/")

def toutf(instr):
    o = ""
    for i in instr:
        if ord(i) < 256:
            o += i
    return o


doCompression = False    

md5sums = {} #key is name, value is dict of all md5sum of given user

for gdi in range(len(allDirs)):
    gameDir = allDirs[gdi]
    match = re.search(r'runs/(.*)\/(.*)-(.*)\/', gameDir)
    if match:
        studentName1 = match.group(2)
        studentName2 = match.group(3)
        if not studentName2 in allGames:
            allGames[studentName2] = {}
        if not studentName1 in allGames:
            allGames[studentName1] = {}

        if not studentName1 in versions:
            versions[ studentName1 ] = {}
        if not studentName2 in versions:
            versions[ studentName2 ] = {}

        if not studentName2 in allGames[studentName1]:
            allGames[studentName1][studentName2] = []
        if not studentName1 in allGames[studentName2]:
            allGames[studentName2][studentName1] = []
        
        if not studentName1 in md5sums:
            md5sums[ studentName1 ] = {}
        if not studentName2 in md5sums:
            md5sums[ studentName2 ] = {}

        files = glob.glob("{}/allGames.p*".format(gameDir))
        print(gameDir,studentName1, studentName2, "files=", len(files))
        print("Loading ",files, ",   processed {:d}/{:d} = {:.2f}".format(gdi, len(allDirs), 100*gdi/len(allDirs)) )
        for name in files:
#            print(name)
            f = open(name,"rb")
            games = pickle.load(f)
            f.close()
            for d in games:
                totalOrigSize += len( d["html"] )
                if doCompression == True:
                    d["html"] = zlib.compress(d["html"].encode(),9)
                totalCompressedSize += len( d["html"] )
                v1 = d["versions"][studentName1]
                v1 = toutf(v1)
                if v1 != "__NA__":
                    versions[studentName1][ v1 ] = [ studentName1, studentName2 ]
                v2 = d["versions"][studentName2]
                v2 = toutf(v2)
                if v2 != "__NA__":
                   versions[studentName2][ v2 ] =  [studentName1, studentName2 ]
                d["LOC"] = { studentName1: [], studentName2: [] }

                if studentName1 in linesCount:
                    d["LOC"][studentName1] = linesCount[studentName1]
                if studentName2 in linesCount:
                    d["LOC"][studentName2] = linesCount[studentName2]

            

                if "md5" in d:
                    for name in d["md5"]:
                        md5value = d["md5"][name]
                        if not md5value in md5sums[name]:
                            md5sums[name][md5value] = 0
                        md5sums[ name ][ md5value ] += 1                            

            allGames[ studentName1 ][studentName2 ] = games                   
        
os.system("rm missingGames.txt")
fo = open("missingGames.txt","wt")      
numGames = {}
for name1 in allGames:
    if not name1 in numGames:
        numGames[name1] = 0
    for name2 in allGames[name1]:
        if not name2 in numGames:
            numGames[name2] = 0

        for rec in allGames[name1][name2]:
            numGames[name1] += 1
            numGames[name2] += 1

        if (name1 != name2) and len( allGames[ name1 ][ name2 ]) != expectedGames:
            fo.write("{} {} {}\n".format(name1,name2, len(allGames[name1][name2])))
fo.close()            


outfile = "allgames.db"                
print(allGames.keys())
print("Saving temp file", outfile)

with open(outfile,"wb") as f:
    pickle.dump(allGames, f)
print("Checking validy of games")

with open("md5sums.p","wb") as f:
    pickle.dump(md5sums, f)

maxNumberOfGames = 0
playedGames = {}
for name in numGames:
    print(name," played ", numGames[name])
    maxNumberOfGames = max( maxNumberOfGames, numGames[name] )
    if not numGames[ name ] in playedGames:
        playedGames[ numGames[name] ] = []
    playedGames[ numGames[name] ].append(name)



for num in playedGames:
    print("Total games", num, " played by", playedGames[num])

runtimes = { name1: { name2:[] for name2 in allGames } for name1 in allGames }
warmTime = {}
for name1 in allGames:
    for name2 in allGames[name1]:
        for game in allGames[name1][name2]:
            if "processTime" in game:
                runtimes[name1][name2].append( game["processTime"] )
                if "warmTime" in game:
                    key = "{}-{}".format(name1, name2)
                    if not key in warmTime:
                        warmTime[key] = []
                    warmTime[ key ].append( game["warmTime"] )

with open("runtimes.p", "wb") as f:
    pickle.dump(runtimes, f)
    

print("Saving runtimes")


fot = open("warmTimes.txt", "wt")

for key in warmTime:
    a = warmTime[key]
    fot.write("{} {}\n".format( str(key), ' '.join(map(str, a) ) ) )
fot.close()
print("Saving warmTimes")


isOK = False
if len(playedGames.keys()) == 1:
    print("Games are OK")
    isOK = True
else:
    print("Some missing games! !!!!!!!!!!!!!!!!!!!!! ")


print("Checking versions: ");
problemNames = []
for user in versions:
    allVersions = list(versions[user].keys())
    print("S[",user,"]: ", allVersions)
    if len(allVersions) > 1:
        problemNames.append(user)
        for version in allVersions:
            print("Version '",version,"' in game: ", versions[user][version], " !!!!!! ")
        isOK = False


os.system("rm replan.sh")
with open("replan.sh", "wt") as f:
    f.write("#!/bin/sh\n")
    f.write("#touching players that dont have enough games")
    for name in numGames:
        f.write("#player " + name + " played " + str( numGames[ name ] ) + " out of " + str(maxNumberOfGames) + "\n")
        if name in problemNames:
            f.write("#User" + name + " has multiple version:\n")

        if numGames[name] != maxNumberOfGames or name in problemNames:
            f.write("echo \"\" >> src/{}/player.py\n".format(name))
            f.write("echo \"#tmp\" >> src/{}/player.py\n".format(name))
        else:
            f.write("#this player is ok\n")
                    
print("Saved replan.sh")






if isOK:
    print("OK, saving into db ")
    os.system("mv {} db/`date +\"%m-%d-%y-%H-%M\".db`".format(outfile))
else:
    print("Problem is versions of users");
    print(problemNames)
    print("DB not saved")

print("Compressiong: before=", int(totalOrigSize/1024), "k, new=", int(totalCompressedSize/1024), "k =" , int(100*totalCompressedSize / totalOrigSize), "%")
print("doCompression=", doCompression, " (if False, maybe pickleAll.py already compressed html .. )")