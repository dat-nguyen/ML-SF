#!/usr/bin/python

"""
    create the xscore conf for input file
"""

import os.path

from libs.ioPDBbind import *

# import constant
from libs.constConf import *

SOURCE_CONF     = '/home/dat/WORK/docking_config/xscore.conf'

#################################################################

def createXScoreConf(CASFyear, proteinID):
    proteinDir  = CASF_PATH[CASFyear]
#   read the exemplary config and create the new config from given param
    outputConf  = 'xscore_' + proteinID + '.conf'
    path = os.path.join(OUTPUT_DIR, 'conf', "PDBbind", CASF_VERSION[CASFyear], 'xscore')
    outputConf  = os.path.join(path, outputConf)

    if not os.path.exists(path): # try to create the dir path first
        os.makedirs(path)
    OUTFILE = open(outputConf, 'w')

    outputScore = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], 'xscore')
    if not os.path.exists(outputScore): # try to create the output dir for scores
        os.makedirs(outputScore)

    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()

    # open file for reading and writing
    INFILE  = open(SOURCE_CONF, 'r')

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'xscore_run_'+CASF_VERSION[CASFyear]+'.sh'), 'a')

    for line in INFILE:
        if line.find('RECEPTOR_PDB_FILE ') > -1:
            line = 'RECEPTOR_PDB_FILE ' + os.path.join(proteinDir, proteinID, proteinID + PROTEIN_SUFFIX + '\n')
        elif line.find('REFERENCE_MOL2_FILE ') > -1:
            line = 'REFERENCE_MOL2_FILE ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX_MOL2+'\n')
        elif line.find('LIGAND_MOL2_FILE ') > -1:
            line = 'LIGAND_MOL2_FILE ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX_MOL2+'\n')
        elif line.find('OUTPUT_TABLE_FILE ') > -1:
            line = 'OUTPUT_TABLE_FILE ' + os.path.join(outputScore, proteinID+'.table\n')
        elif line.find('OUTPUT_LOG_FILE ') > -1:
            line = 'OUTPUT_LOG_FILE ' + os.path.join(outputScore, proteinID+'.log\n')
        OUTFILE.write(line)

    # write sh script
    SHFILE.write('xscore ' + outputConf + '\n')

    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

def createXscoreScore(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    #indexFile   = CASF_CORE_INDEX[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    #print(len(data.keys()))
    #print(data['3ckz'])
    for entry in data.keys():
        if (entry=="3ckz"): print(data[entry])
        if os.path.isdir(os.path.join(proteinDir, entry)):
            proteinFile = entry + PROTEIN_SUFFIX
            ligandFile  = entry + LIGAND_SUFFIX_MOL2
            if os.path.exists(os.path.join(proteinDir, entry, proteinFile)) and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
                # only create config file if the ligand and the protein exist
                createXScoreConf(CASFyear, entry)
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                quit()
    print('Finish creating xscore for {0}.'.format(CASFyear))

#createXscoreScore('2007')
createXscoreScore('2012')
createXscoreScore('2013')
createXscoreScore('2014')


