#!/usr/bin/env python3
import json, glob, sys, pickle, os

prefixDir = "src"

#this script assumes that alp-hive contains actual source codes


dirs = glob.glob("{}/*".format(prefixDir))

tmpFile = "countLines.json"
outfile = "linesCount.pickle"

counts = {}

for dirname in dirs:
    studentName = dirname.replace("{}".format(prefixDir),"").replace("/","")
    print("Processing", dirname, " student:", studentName)

    os.system("pygount --format=json -o {} --suffix=py  {}".format(tmpFile, dirname))
    f = open(tmpFile)
    data = json.load(f)
    for l in data["languages"]:
        if l["language"] == "Python":
            lineCnt = l["sourceCount"]
            commentsCount = l["documentationCount"]
            counts[studentName] = [ lineCnt, commentsCount ]
            print("Counting files in", dirname, ": lines", lineCnt, ", comments", commentsCount)
    f.close()

print("Saving count lines into ", outfile)
f = open(outfile,"wb")
pickle.dump(counts, f)
f.close()
os.system("rm {}".format(tmpFile))    