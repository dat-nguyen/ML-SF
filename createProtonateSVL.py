#!/usr/bin/python

"""
    create the 
"""

import  os.path

import  ioMisc

PROTEIN_DIR     = '/home/dat/WORK/DB/PDBbind/'

OUTPUT_DIR      = '/home/dat/WORK/output/'

i = 5

PROTEIN_LIST    = ['/home/dat/WORK/output/PDBbind_test12.txt',
                   #'/home/dat/WORK/output/PDBbind_training12.txt',
                   '',
                   '',
                   '',
                   '',
                   '/home/dat/WORK/output/PDBbind_test07.txt']
lPROTEIN_STATUS  = ['unprepared', 'prepared']

lPROTEIN_DB      = ['PDBbind', '']

lPROTEIN_DB_VER  = ['v2012', 'v2007']

PROTEIN_SUFFIX   = '_protein.pdb'
LIGAND_SUFFIX    = '_ligand.mol2'  

proteinDict = ioMisc.readDictFile(PROTEIN_LIST[0]) 

proteinDir  = os.path.join(PROTEIN_DIR, lPROTEIN_DB_VER[0])

print proteinDir

OUTFILE = open(os.path.join(OUTPUT_DIR, 'removeWater.txt'), 'w')

for entry in proteinDict.keys():
    if os.path.isdir(os.path.join(proteinDir, entry)):
        proteinFile = entry + PROTEIN_SUFFIX
        if os.path.exists(os.path.join(proteinDir, entry, proteinFile)):
            # only create protein PDB file if the protein exist
            #OUTFILE.write("runProtonate3D [DBPath, \""+entry+"\"];\n")
            OUTFILE.write("removeWater [DBPath, \""+entry+"\"];\n")
            #print "runProtonate3D [DBPath, \""+entry+"\"];"
        else:
            print "File not found ", proteinFile, ' in ', os.path.join(proteinDir, entry)
            quit()

OUTFILE.close()

