def get_objects():
    return []

def get_referrers(*objs):
    return []
generate.py
#!/usr/bin/env python3

import sys, os, glob, re, hashlib, pickle, random

if len(sys.argv) < 2:
    print("usage", sys.argv[0], " <runAll 0/1> [missingGames.txt]")
    quit()

runAllPlayers = int( sys.argv[1] )
missingGamesFile = ""
if len(sys.argv) == 3:
    missingGamesFile = sys.argv[2]


srcDir = "src-processed"
runSrcDir = "runs-src"
runDir = "runs"
gameDir = "/storage/praha1/home/vonasek/alp/streky/"
homeDir = "/storage/praha1/home/vonasek"
            
expectedRuntimeDefault = 15  #lengs of ONE game in seconds
runTimePerJob = 12*60 #in seconds


playerFile = "player.py"

missingGames = []
if missingGamesFile != "":
    with open(missingGamesFile,"rt") as f:
        for line in f:
            missingGames.append( line.strip().split() )
print("Loaded", len(missingGames),"missing games records")

def loadPlayer(filename):
    res = ''
    if os.path.isfile(filename):
        try:
            f = open(filename,"rt")
            lines = f.readlines()
            res = ''.join(lines)
        except:
            pass
    return res            

def filemdsum(filename):
    if os.path.isfile(filename):
        return hashlib.md5(open(filename,"rb").read()).hexdigest()
    else:
        return hashlib.md5(b"none").hexdigest()


players = {}

for directory in glob.glob("{}/*".format(srcDir)):
    print("directory", directory)
    res = re.search("{}/(.*)".format(srcDir), directory)
    if res and len(res.groups()) > 0:
        playerName = res.groups()[0]
        if playerName in players:
            print("Error when parsing", directory, ": player name already in player!")
            quit()
        md5 = filemdsum("{}/player.py".format(directory))
        players[ playerName ] = [ directory, md5 ]

#check m5dsum of already played games
md5sums = {}
if os.path.isfile("md5sums.p"):
    md5sums = pickle.load( open("md5sums.p", "rb" ) )

print("Loaded MD5", md5sums)

runtimes = {}
if os.path.isfile("runtimes.p"):
    runtimes = pickle.load( open("runtimes.p", "rb") )
print("Loaded", len(runtimes), "runtimes values")

computeGames = { name: { name2: None for name2 in players if name2 != name } for name in players }

       

changeInPlayer = {}

for name1 in players:
    changeInPlayer[ name1 ] = False
    dirname, md5new = players[ name1 ]

    print("Codes", name1, ": new=", md5new, ", old=", md5sums[name1] if name1 in md5sums else "unknown", end=" | ")
    
    if (name1 in md5sums) and (md5new in md5sums[name1]) and (len(md5sums[name1]) == 1):
        print("SAME")
    else:
        print("DIFFERENT")
        changeInPlayer[name1] = True
    if runAllPlayers == 1:
            changeInPlayer[ name1 ] = True

    for name2 in players:
        if name2 == name1:
            continue
        outdir = "{}/{}/{}-{}".format(runDir, name1, name1, name2)
        os.system("mkdir -p {}".format(outdir))
        outfile = "{}/allGames.p".format(outdir)
        if not os.path.isfile(outfile):
            computeGames[name1][name2] = outdir #outdir ia not used anymore
            computeGames[name1][name2] = True 

for item in missingGames:
    name1, name2, value = item
    if name1 in computeGames and name2 in computeGames:
        computeGames[name1][name2] = True
        print("Recomputing", name1, "vs", name2, " according to missing games")
    else:
        print("Got information about missing game", name1, "vs", name2, " but these records are not amongst current users!! ")
        print("!!!!!!!")
 


os.system("tar czhf streky-all.tar.gz *.py src-processed")

cmds = []

for name1 in players:
    for name2 in players:
        if name1 == name2:
            continue
        if computeGames[name1][name2] != None or changeInPlayer[name1] or changeInPlayer[name2]:
                
            cmd = " ### game {} vs {}, reason: missing game {}, change in {}={}, change in {}={}\n".format(name1, name2, computeGames[name1][name2],name1, changeInPlayer[name1], name2, changeInPlayer[name2])
            cmd += "cd $SCRATCHDIR\n"
            cmd += "mkdir {}-{}\n".format(name1, name2)
            cmd += "cd {}-{}\n".format(name1, name2)
            cmd += "cp -r ../src-processed/{} s123a\n".format(name1)
            cmd += "cp -r ../src-processed/{} s123b\n\n".format(name2)
            cmd += "touch s123a/__init__.py\n"
            cmd += "touch s123b/__init__.py\n"
            for trial in range(10):
                cmd += "rm -rf __pycache__ s123a/__pycache__ s123b/__pycache__\n"
                cmd += "cp ../*.py . \n"
                cmd += "cp ../inspect.py ../gc.py s123a\n"
                cmd += "cp ../inspect.py ../gc.py s123b\n"
                cmd += "python3 -B game.py out.{} {} {} {} doremove\n\n".format(trial, trial, name1, name2)

            cmd += "python3 ../pickleAll.py\n"
            cmd += "rm {}/{}/{}/{}-{}/allGames.p\n".format(gameDir,runDir,name1, name1, name2)
            cmd += "cp -f allGames.p {}/{}/{}/{}-{}/\n".format(gameDir, runDir, name1, name1, name2)
            cmd += "cd $SCRATCHDIR\n"
            cmd += "rm -rf {}-{}\n".format(name1, name2)

            estimatedRuntime = -1
            if name1 in runtimes and name2 in runtimes[name1]:
                vals = runtimes[name1][name2] + [-1]
                estimatedRuntime = max( estimatedRuntime, max(vals) )
            if name2 in runtimes and name1 in runtimes[name2]:
                vals = runtimes[name2][name1] + [-1]
                estimatedRuntime = max( estimatedRuntime , max(vals) )
#            print("A",name1, name2, "time", estimatedRuntime, expectedRuntimeDefault)

            if estimatedRuntime < 0:
                estimatedRuntime = expectedRuntimeDefault
            estimatedRuntime *= 10
#            print("B",name1, name2, "time", estimatedRuntime)

            cmds.append( [ cmd, name1, name2, estimatedRuntime ] )



print("Generated", len(cmds), "commands")


pbsPrefix="""#!/bin/bash
#PBS -l select=1:ncpus=1:mem=1400mb:scratch_local=1gb
#PBS -l walltime=01:59:00
#PBS -N {jobName}

un=`uname -a`
module add python36-modules/gcc
trap 'clean_scratch' TERM EXIT
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{homeDir}/opt/lib
export PATH={homeDir}/opt/bin:$PATH
cd $SCRATCHDIR
export PYTHONIOENCODING='utf-8'

echo copying .tar.gz
date
cp {gameDir}/streky-all.tar.gz . 
tar xfz streky-all.tar.gz 
echo \"end of copying .tar.gz\"
date
"""


isJobAssigned = [ False for _ in range(len(cmds)) ]

batches = []
while False in isJobAssigned:
    
    sumTime = 0
    trials = len(isJobAssigned) // 2
    trial = 0
    batch = []
    while sumTime < runTimePerJob and trial < trials:
        trial += 1
        isfreejobsidx = [ i for i in range(len(isJobAssigned)) if isJobAssigned[i] == False ]
        r = random.sample(isfreejobsidx,1)[0]
        
        lastround = False
        if len([ 1 for i in isJobAssigned if i == False ]) < len(isJobAssigned) / 20:
            lastround = True

        if sumTime + cmds[r][3] < runTimePerJob or lastround:
            batch.append(r)
            isJobAssigned[r] = True
            sumTime += cmds[r][3]
        if lastround:
            break
    if len(batch) > 0:
        batches.append([batch, sumTime])
        print("Generated", len(batches), ", remaininmg", len([ 1 for i in isJobAssigned if i == False ] ), ", last batch has", len(batches[-1][0]), " games     ", end="\r")


print("Created", len(batches), "batches from total", len(cmds), "commands, estimated total runtime is ", sum([item[1] for item in batches]), "s")
if False in isJobAssigned:
    print("Error, some jobs are not assigned!")
    quit()

"""
for ci in range(len(cmds)):
    cmdString, name1, name2,estimatedRuntime = cmds[ci]
    f = open("cmd.{}.sh".format(ci), "wt")
    f.write(pbsPrefix.format(jobName="trx-"+str(ci), gameDir = gameDir, homeDir = homeDir ) )
    f.write("#Expected runtime {}s\n".format(estimatedRuntime))
    f.write("\n#cmds:\n\n")
    f.write(cmdString)
    f.close()
"""

print("Generating cmd files")
for batchi in range(len(batches)):
    jobsidx, runtime = batches[batchi]
#    print("Generating", batchi, " estimated runtime", runtime)
    f = open("cmd.{}.sh".format(batchi), "wt")

    f.write(pbsPrefix.format(jobName="trx-"+str(cmds[jobsidx[0]][1]) + ":"+ str(cmds[jobsidx[0]][2]), gameDir = gameDir, homeDir = homeDir ) )
    f.write("#Expected runtime of whole batch {}s, num batches={}\n".format(runtime, len(jobsidx)))
    for ji in jobsidx:
        cmdString, name1, name2, estimatedRuntime = cmds[ji]
        f.write("#Command {}/{}, estimated runtime={}s\n".format(ji,len(cmds),estimatedRuntime))
        f.write(cmdString)
        f.write("#end of command {}/{}\n\n".format(ji, len(cmds)))
    f.close()
print("End of generate")