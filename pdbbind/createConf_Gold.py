#!/usr/bin/python

"""
    create the gold config for gold_auto
"""

import os.path

from libs.ioPDBbind import *

# import constant
from libs.constConf import *

SOURCE_CONF = '/home/dat/WORK/docking_config/gold.conf'

#################################################################

def createGoldConf(CASFyear, proteinID, score):
    proteinDir  = CASF_PATH[CASFyear]
#   read the exemplary config and create the new config from given param
    outputConf  = 'gold_' + proteinID + '_' + score + '.conf'
    path = os.path.join(OUTPUT_DIR, "conf", "PDBbind", CASF_VERSION[CASFyear], "gold", score)
    outputConf  = os.path.join(path, outputConf)
    print(outputConf)
    if not os.path.exists(path): # try to create the dir path first
        os.makedirs(path) 
    OUTFILE = open(outputConf, 'w')
    
    outputScore = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], "gold", score)
    if not os.path.exists(outputScore): # try to create the output dir for scores
        os.makedirs(outputScore)
    
    # open conf file 
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()
    
    # open file for reading and writing 
    INFILE  = open(SOURCE_CONF, 'r')
    
    SHFILE  = open(os.path.join(OUTPUT_DIR, 'gold_run_'+CASF_VERSION[CASFyear]+'_'+score+'.sh'), 'a')
    
    for line in INFILE:
        if line.find('cavity_file =') > -1:
            line = 'cavity_file = ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX + EXT_MOL2 + '\n')
        elif line.find('ligand_data_file') > -1:
            line = 'ligand_data_file ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX + EXT_MOL2) + ' 10\n'
        elif line.find('directory =') > -1:
            line = 'directory = ' + os.path.join(outputScore, proteinID + '\n')
        elif line.find('protein_datafile =') > -1:
            line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + PROTEIN_SUFFIX + EXT_PDB + '\n')
#            if ((proteinID == '1xgj') or (proteinID == '2pu2')) and (proteinStatus == 1): #prepared
#                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_proton_f.pdb\n')
#            if ((proteinID == '1w3l')) and (proteinStatus == 0): #unprepared
#                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_f.pdb\n')
#            if ((proteinID == '1b9j')) and (proteinStatus == 0) and (CASFyear=="v2007"): #unprepared
#                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_del.pdb\n')
#            if ((proteinID == '1b7h')) and (proteinStatus == 0) and (CASFyear=="v2007"): #unprepared
#                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_del.pdb\n')

        elif line.find('gold_fitfunc_path =') > -1:
            line = 'gold_fitfunc_path = ' + score + '\n'
        OUTFILE.write(line)
    
    # write sh script
    SHFILE.write('gold_auto ' + outputConf + '\n')
    
    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

def createGoldScore(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_CORE_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)

    for score in GOLD_DOCKING_SCORE:
        for entry in data.keys():
            if os.path.isdir(os.path.join(proteinDir, entry)):
                proteinFile = entry + PROTEIN_SUFFIX + EXT_PDB
                ligandFile  = entry + LIGAND_SUFFIX + EXT_MOL2
                if os.path.exists(os.path.join(proteinDir, entry, proteinFile)) and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
                    # only create config file if the ligand and the protein exist
                    createGoldConf(CASFyear, entry, score)
                else:
                    print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                    quit()
            else:
                print(os.path.join(proteinDir, entry) + " is not exist\n")
        print('Finish creating gold_run for '+ score)

CASFyear = '2007'
#createGoldScore(CASFyear)
#createGoldScore('2012')
#createGoldScore('2013')

# test code
#proteinDir  = CASF_PATH[CASFyear]
#indexFile   = CASF_REFINED_INDEX[CASFyear]
#data = parse_index(proteinDir, indexFile)
#print(len(data.keys()))

#data = ioPDBbind.parse_index("/home/dat/WORK/DB/PDBbind/v2012-refined/", "/home/dat/WORK/DB/PDBbind/v2012-refined/INDEX_core_cluster.2012")

#data = ioPDBbind.parse_index("/home/dat/WORK/DB/PDBbind/v2007/", "/home/dat/WORK/DB/PDBbind/v2007/INDEX.2007.refined.data")
#print(data['2fdp']['year'])