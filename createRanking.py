__author__ = 'dat'

'''
\TODO: optimize + write comments

'''

import os.path

__author__ = 'dat'
#!/usr/bin/python

##########################################################
#
#    create the % ratio of ranking from a given score
#
##########################################################


import os.path
import csv
from libs.ioPDBbind import *
from libs.ioScore import *
import libs.libRank

#from libs import libRank, ioPDBbind
#from libs.ioPDBbind import *

#OUTPUT_DIR  = "/Users/knight/MyClouds/scores/"
OUTPUT_DIR = "/home/dat/WORK/output/scores/"

CVscoresList    = ["plp","goldscore","chemscore","asp","HPScore","HMScore","HSScore","DSX","DrugScore","pScore","PMF"]
MLscoresList    = ["RF","BRT","SVM","MLR"]
ELscoresList    = ["RoF-RoT","RoF-REPT","Bagging-RoT","Bagging-REPT","RandSS-RoT","RandSS-REPT"]

scoresList = {"ELscores" : ELscoresList,
              "MLscores" : MLscoresList,
              "scores"   : CVscoresList}

rankingCount = { '123':0, '132':0, '213':0, '231':0, '312':0, '321':0 }

def calcRanking(score, scoresMatrix, CASFyear):
    # reset the ranking count
    rankingCount = { '123':0, '132':0, '213':0, '231':0, '312':0, '321':0 }
    # reset the clusterDict
    clusterDict         = createClusterDictFromYear(CASFyear)
    proteinDict         = parseIndexFromYear(CASFyear)

    for proteinID in proteinDict.keys():
        cluster = proteinDict[proteinID]["cluster"]
        proteinInCluster = clusterDict[cluster]
        for i in range(len(proteinInCluster)):
            if proteinInCluster[i] == proteinID:
                clusterDict[cluster][i] = scoresMatrix[proteinID][score]
    for value in clusterDict.values():
        #print(value)
        tmp = ''.join(str(i+1) for i in libs.libRank.rank_simple(value) )
        #print(tmp)
        #tmp = ''.join(str(i+1) for i in libRank.rank(map(float, value)))
#        tmp = ''.join(str(i+1) for i in libs.libRank.rank(map(abs, map(float, value))))
        #if (tmp != '123'):
#            print(value, libRank.rank(value))
        rankingCount[tmp] = rankingCount[tmp] + 1

#    print(rankingCount)

    totalCluster = len(clusterDict.keys())

    #OUTFILE = open(outFile, 'a')
    #OUTFILE.write(aScore + '\t')
    for rank in sorted(rankingCount.keys()):
        ranking = float(rankingCount[rank])/totalCluster * 100
#        print(rank, ranking)
        #OUTFILE.write(str(ranking)+'\t')
    #OUTFILE.write('\n')
    #OUTFILE.close()
    return round(float(rankingCount['123']+rankingCount['132'])/totalCluster*100, 2)
    #return round(float(rankingCount['123'])/totalCluster*100, 2)


def createRankingScore(CASFyear):
    scoresMatrix = {}
    #CSVinput  = os.path.join(OUTPUT_DIR, CASF_NAME[CASFyear]+"_core_"+"ELscores_elementsv2-SIFt.csv")

    rankingValues = []
    for scoreType in sorted(scoresList.keys()):
        if scoreType == "scores":
            CSVinput  = os.path.join(OUTPUT_DIR, CASF_NAME[CASFyear]+"_core_"+scoreType+".csv")
        else:
            CSVinput  = os.path.join(OUTPUT_DIR, CASF_NAME[CASFyear]+"_core_"+scoreType+"_elementsv2-SIFt-xscore.csv")

        with open(CSVinput, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                scoresMatrix[row['PDB']] = row

        for score in scoresList[scoreType]:
            rankingValues.append(calcRanking(score, scoresMatrix, CASFyear) )
            #print(score, calcRanking(score, scoresMatrix, CASFyear))
    return (rankingValues)

############# MAIN PART ########################
if __name__=='__main__':
    '''
    '''
    #CASFyear = '2007'
    ranking = {}
    for CASFyear in CASF_NAME.keys():
        ranking[CASF_NAME[CASFyear]] = createRankingScore(CASFyear)
    scoreNames = []
    for scoreType in sorted(scoresList.keys()):
        scoreNames = scoreNames + scoresList[scoreType]

    CSVfile     = os.path.join(OUTPUT_DIR, "Ranking_1xx_core.csv")
    #CSVfile     = os.path.join(OUTPUT_DIR, "Ranking_123_core.csv")
    writeScoreCSV(scoreNames, ranking, outFile=CSVfile)



    #print(ioPDBbind.createClusterDictFromYear('2007'))

