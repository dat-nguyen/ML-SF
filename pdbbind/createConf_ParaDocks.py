#!/usr/bin/python

"""
    create the xscore conf for input file
"""

import os.path

from libs.ioPDBbind import *
from libs.constConf import *

SOURCE_CONF     = '/home/dat/WORK/docking_config/para_run.xml'

def createParaDocksConf(CASFyear, proteinID):
    proteinDir  = CASF_PATH[CASFyear]
#   read the exemplary config and create the new config from given param
    outputConf  = 'paradocks_' + proteinID + '.xml'
    path = os.path.join(OUTPUT_DIR, 'conf', "PDBbind", CASF_VERSION[CASFyear], 'paradocks')
    outputConf  = os.path.join(path, outputConf)
    
    if not os.path.exists(path): # try to create the dir path first
        os.makedirs(path) 
    OUTFILE = open(outputConf, 'w')
    
    outputScore = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], 'paradocks', proteinID)
    if not os.path.exists(outputScore): # try to create the output dir for scores
        os.makedirs(outputScore)
    
    # open conf file 
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()
    
    # open file for reading and writing 
    INFILE  = open(SOURCE_CONF, 'r')

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'para_run_'+CASF_VERSION[CASFyear]+'.sh'), 'a')

    proteinFile = os.path.join(proteinDir, proteinID, proteinID + PROTEIN_SUFFIX)

    MOL2outputDir = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], "mol2")
    if not os.path.exists(MOL2outputDir):
        os.makedirs(MOL2outputDir)
    proteinFileMOL2 = os.path.join(MOL2outputDir, proteinID + PROTEIN_SUFFIX_MOL2)

    # convert PDB to MOL2
    SHFILE.write("babel -ipdb {0} -omol2 {1}\n".format(proteinFile, proteinFileMOL2))

    for line in INFILE:
        if line.find('<Name>1A0Q') > -1:
            line = '<Name>' + proteinID + '_PROTEIN</Name>\n'
        elif line.find('<File>/mnt/') > -1:            
            line = '<File>' + proteinFileMOL2 + '</File>\n'
        elif line.find('<File>/home/') > -1:
            line = '<File>' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX_MOL2) + '</File>\n'
        elif line.find('<OutputPath>') > -1: # <OutputPath>/home/dat/WORK</OutputPath>
            line = '<OutputPath>' + outputScore + '</OutputPath>\n'
        OUTFILE.write(line)
    
    # write sh script
    SHFILE.write('/mnt/zeus/dat/WORK/dev/paradocks/build/bin/paradocks ' + outputConf + '\n')
    
    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

def createParaDocksScore(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_CORE_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    for entry in data.keys():
        if os.path.isdir(os.path.join(proteinDir, entry)):
            proteinFile = entry + PROTEIN_SUFFIX
            ligandFile  = entry + LIGAND_SUFFIX_MOL2
            if os.path.exists(os.path.join(proteinDir, entry, proteinFile)) and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
                # only create config file if the ligand and the protein exist
                createParaDocksConf(CASFyear, entry)
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                quit()
        else:
            print(os.path.join(proteinDir, entry) + " is not exist\n")

    print("Finish creating paradocks xml for {0}.".format(CASFyear))


createParaDocksScore('2007')
#createParaDocksScore('2012')
#createParaDocksScore('2013')