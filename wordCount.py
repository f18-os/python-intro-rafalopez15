import sys
import re
import os
import subprocess

inputfile = sys.argv[1]
outputfile = sys.argv[2]

wordList = {}

with open(inputfile, 'r') as inputfile:
    for line in inputfile:
        line = line.strip()
        #make all lower case
        line = line.lower()
        #remove any punctuation from line
        word = re.findall(r"[\w']+", line)
        for w in word:
            if w not in wordList:
                wordList[w] = 1
            else:
                wordList[w] += 1

sortedWords = sorted(wordList.items())

with open(outputfile, 'w') as outputfile:
    for item in sortedWords:
        outputfile.write("%s %d\n" % item)