#!/usr/bin/python

"""
    create the drugscore conf for input file
"""

#/prog/scoring/drugscore/2011/dsx_linux_64.lnx -P /home/dat/WORK/DB/PDBbind/v2012/1px4/1px4_protein.pdb -L /home/dat/WORK/DB/PDBbind/v2012/1px4/1px4_ligand.mol2 -D /prog/scoring/drugscore/2011/pdb_pot_0511/

import os.path

from libs.ioPDBbind import *
# import constant
from libs.constConf import *

def createDrugScore(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_CORE_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)

    OUTFILE = open(os.path.join(OUTPUT_DIR, 'dsx_run_'+CASF_VERSION[CASFyear]+'.sh'), 'w')

    outputDir = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], 'dsx')

    OUTFILE.write('cd '+outputDir+'\n')

    if not os.path.exists(outputDir): # try to create the dir path first
        os.makedirs(outputDir)

    for entry in data.keys():
        if os.path.isdir(os.path.join(proteinDir, entry)):
            proteinFile = entry + PROTEIN_SUFFIX
            ligandFile  = entry + LIGAND_SUFFIX_MOL2
            proteinFileWithPath = os.path.join(proteinDir, entry, proteinFile)
            ligandFileWithPath  = os.path.join(proteinDir, entry, ligandFile)
            if os.path.exists(proteinFileWithPath) and  os.path.exists(ligandFileWithPath):
                # only create config file if the ligand and the protein exist
                OUTFILE.write('/prog/scoring/drugscore/2011/dsx_linux_64.lnx -P '+ proteinFileWithPath + ' -L ' + ligandFileWithPath + ' -D /prog/scoring/drugscore/2011/pdb_pot_0511\n')
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                quit()

    print('Finish creating dsx run.')

    OUTFILE.close()

#createDrugScore('2012')
createDrugScore('2013')
