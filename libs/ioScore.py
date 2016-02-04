'''
Created on 17.04.2013

@author: dat

read and write score from log files
'''

import os.path


def readGOLDScore(scoreFile):
    # open score file
    if not os.path.exists(scoreFile):
        print("File not found ",scoreFile)
        quit()

    SFILE = open(scoreFile, 'r')

    # read 7 first lines
    for i in range(7):
        SFILE.readline()

    line = SFILE.readline()
    try:
        score = float(line.split(None)[0])
    except Exception:
        score = 'NA'
        print("Error detected in ",scoreFile)
        print(line)

    SFILE.close()
    return score

def readGOLDScore_old(scoreFile):
    # open score file 
    if not os.path.exists(scoreFile):
        print("File not found ",scoreFile)
        quit()
    
    SFILE = open(scoreFile, 'r')

    # read 3 first lines
    for i in range(3):    
        SFILE.readline()
        
    line = SFILE.readline()
    try:
        score = float(line.split(None)[4])
    except Exception:
        score = 'NA'
        print("Error detected in ",scoreFile)
        print(line)
        
    SFILE.close()
    return score

def readXScore(scoreFile):
    # open score file 
    if not os.path.exists(scoreFile):
        print("File not found ",scoreFile)
        quit()
    
    SFILE = open(scoreFile, 'r')
    SFILE.readline() # skip the first line
    line = SFILE.readline()
    try:
        HPScore = float(line.split()[4])
        HMScore = float(line.split()[5]) 
        HSScore = float(line.split()[6])
        score = (HPScore, HMScore, HSScore)
    except Exception:
        score = ('NA', 'NA', 'NA')#(0, 0, 0)
        print("Error detected in ",scoreFile)
        print(line)
        
    SFILE.close()
    return score

def readDSXScore(scoreFile):
    # open score file 
    if not os.path.exists(scoreFile):
        print("File not found ",scoreFile)
        quit()
    
    SFILE = open(scoreFile, 'r')
    i = 0
    score = 0
    for line in SFILE.readlines():
        if (i==32):
            #print(line.split('|'))
            try:
                score = float(line.split('|')[3])
            except Exception:
                score = 'NA'
                print("Error detected in ",scoreFile)
                print(line)
        i = i+1 
        
    SFILE.close()
    return score
    
def readPARAScore(scoreFile):
    # open score file 
    if not os.path.exists(scoreFile):
        print("File not found ",scoreFile)
        return ('NA', 'NA', 'NA')   
        #quit()
    
    SFILE = open(scoreFile, 'r')
    # read 3 first lines
    for i in range(3):    
        SFILE.readline()
        
    line = SFILE.readline()
    try:
        pScore  = float(line.split('|')[3])
        PMF     = float(line.split('|')[7]) 
        DrugScore = float(line.split('|')[11])
        score = (pScore, PMF, DrugScore)
#        print line.split('|')        
    except Exception:
        score = ('NA', 'NA', 'NA')
        print("Error detected in ",scoreFile)
        print(line)

        
    SFILE.close()
    return (score)

def readGLIDEScore(scoreFile):
    # open score file
    if not os.path.exists(scoreFile):
        print("File not found ",scoreFile)
        return ('NA', 'NA', 'NA')
        #quit()

    SFILE = open(scoreFile, 'r')
    # read 13 first lines
    for i in range(13):
        SFILE.readline()

    line = SFILE.readline()
    try:
        score  = float(line.split()[2])
    except Exception:
        score = ('NA', 'NA', 'NA')
        print("Error detected in ",scoreFile)
        print(line)

    SFILE.close()
    return (score)


def writeScoreCSV(scoreList, scoreDict, outFile):
    import csv
    writer = csv.writer(open(outFile, 'w', newline=''))
    writer.writerow(scoreList)
    for key, value in scoreDict.items():
        writer.writerow([key] + value)

def writeRankingCSV(scoreList, scoreDict, outFile):
    import csv
    writer = csv.writer(open(outFile, 'w', newline=''))
    writer.writerow(scoreList)
    for key, value in scoreDict.items():
        writer.writerow([key] + value)
