#!/usr/bin/python

"""
    create the xscore conf for input file
"""

import os.path

from libs import libIO

SOURCE_CONF     = '/home/dat/WORK/scripts/para_run.xml'
PROTEIN_DIR     = '/home/dat/WORK/DB/CSAR_NRC_HiQ_Set_24Sept2010/Separation/'
PROTEIN_LIST    = '/home/dat/WORK/DB/CSAR_NRC_HiQ_Set_24Sept2010/Separation/set1.txt'

OUTPUT_DIR      = '/home/dat/WORK/output/'

lPROTEIN_STATUS  = ['unprepared', 'prepared']
lPROTEIN_DB      = ['PDBbind', 'CSAR']
lPROTEIN_DB_VER  = ['set1', 'set2']
lPROTEIN_SUFFIX   = ['_protein.mol2', '_protein_proton.mol2',]
LIGAND_SUFFIX    = '_ligand.mol2'  

i = 0
proteinDir  = os.path.join(PROTEIN_DIR, lPROTEIN_DB_VER[i])

def createParaDocksConf(proteinStatus, proteinDB, DBver, proteinID):
#   read the exemplary config and create the new config from given param
    outputConf  = 'paradocks_' + proteinID + '.xml'
    path = os.path.join(OUTPUT_DIR, 'conf', lPROTEIN_STATUS[proteinStatus], proteinDB, DBver, 'paradocks')
    outputConf  = os.path.join(path, outputConf)
    
    if not os.path.exists(path): # try to create the dir path first
        os.makedirs(path) 
    OUTFILE = open(outputConf, 'w')
    
    outputScore = os.path.join(OUTPUT_DIR, lPROTEIN_STATUS[proteinStatus], proteinDB, DBver, 'paradocks', proteinID)
    if not os.path.exists(outputScore): # try to create the output dir for scores
        os.makedirs(outputScore)
    
    # open conf file 
    if not os.path.exists(SOURCE_CONF):
        print "File not found ", SOURCE_CONF   
        quit()
    
    # open file for reading and writing 
    INFILE  = open(SOURCE_CONF, 'r')
    
    SHFILE  = open(os.path.join(OUTPUT_DIR, 'para_run_'+lPROTEIN_STATUS[proteinStatus]+'.sh'), 'a')
    
    for line in INFILE:
        if line.find('<Name>1A0Q') > -1:
            line = '<Name>' + proteinID + '_PROTEIN</Name>\n'
        elif line.find('<File>/mnt/') > -1:            
            line = '<File>' + os.path.join(proteinDir, proteinID, proteinID + lPROTEIN_SUFFIX[proteinStatus] + '</File>\n')
        elif line.find('<File>/home/') > -1:
            line = '<File>' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX + '</File>\n')
        elif line.find('<OutputPath>') > -1: # <OutputPath>/home/dat/WORK</OutputPath>
            line = '<OutputPath>' + outputScore + '</OutputPath>\n'
        OUTFILE.write(line)
    
    # write sh script
    SHFILE.write('paradocks ' + outputConf + '\n')
    
    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

proteinDict = libIO.readDictFile(PROTEIN_LIST)

proteinStatus = 0 # unprepared

for entry in proteinDict.keys():
    if os.path.isdir(os.path.join(proteinDir, entry)):
        proteinFile = entry + lPROTEIN_SUFFIX[proteinStatus]
        ligandFile  = entry + LIGAND_SUFFIX
        if os.path.exists(os.path.join(proteinDir, entry, proteinFile)) and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
            # only create config file if the ligand and the protein exist
            #createGoldConf(lPROTEIN_STATUS[0], lPROTEIN_DB[0], lPROTEIN_DB_VER[0], entry, lSCORE[0])
            createParaDocksConf(proteinStatus, lPROTEIN_DB[1], lPROTEIN_DB_VER[i], entry)
        else:
            print "File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry)
            quit()
    else:
        print os.path.join(proteinDir, entry) + " is not exist\n"

print 'Finish creating paradocks xml.'

