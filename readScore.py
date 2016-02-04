#!/usr/bin/python

import os.path

from libs.ioScore import *
from libs.ioPDBbind import *
from libs.constConf import *

scoreListGOLD   = ['plp', 'goldscore', 'chemscore', 'asp']
scoreListXSCORE = ['HPScore', 'HMScore', 'HSScore']
scoreListGLIDE  = ['SP', 'XP']
scoreListPARA   = ['DrugScore', 'pScore', 'PMF']

CASFyear = '2013'

def readScore(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_CORE_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)

    outputDir  = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear])
    scoreDict   = {}

    for protein in data.keys():
        scoreDict[protein] = [float(data[protein]['pKx'])]
        ##### read score from GOLD #####
        for score in scoreListGOLD:
            #scoreFile = os.path.join(outputDir, 'gold', score, protein, 'rescore.log')
            scoreFile = os.path.join(outputDir, 'gold', score, protein, 'bestranking.lst')
            readScore   = readGOLDScore(scoreFile)
            #print protein, ' ', score,'\t', readScore
            scoreDict[protein].append(readScore)
        ##### read score from XScore #####
        scoreFile = os.path.join(outputDir, 'xscore', protein+'.table')
        readScore = readXScore(scoreFile)
        for eachScore in readScore:
            scoreDict[protein].append(eachScore)
        ##### read score from DSX #####
        scoreFile = os.path.join(outputDir, 'dsx', 'DSX_'+protein+'_protein_prep_'+protein+'_ligand.txt')
        readScore   = readDSXScore(scoreFile)
        scoreDict[protein].append(readScore)
        ##### read score from ParaDocks #####
        scoreFile = os.path.join(outputDir, 'paradocks', protein ,'ParaDockS_results.table')
        readScore = readPARAScore(scoreFile)
        for eachScore in readScore:
            scoreDict[protein].append(eachScore)

    scoreList   = ['PDB','experimental'] + scoreListGOLD + scoreListXSCORE + ['DSX'] + scoreListPARA
    CSVfile     = os.path.join(OUTPUT_DIR, "scores", CASF_NAME[CASFyear]+'_core_scores.csv')
    #print(CSVfile)
    writeScoreCSV(scoreList, scoreDict, outFile=CSVfile)

readScore('2007')
readScore('2012')
readScore('2013')