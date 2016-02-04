#!/usr/bin/python

"""
    create
"""

import  os.path

from libs import libIO

PROTEIN_DIR     = '/home/dat/WORK/DB/CSAR_NRC_HiQ_Set_24Sept2010/Structures/'
OUT_DIR         = '/home/dat/WORK/DB/CSAR_NRC_HiQ_Set_24Sept2010/Separation/'

lSETS           = ['set1', 'set2']

OUTFILE = open(os.path.join(OUT_DIR, 'separateComplex.txt'), 'w')

for aSet in lSETS:
    INpath  = os.path.join(PROTEIN_DIR, aSet)
    OUTpath = os.path.join(OUT_DIR, aSet) 
    OUTLIST = open(os.path.join(OUT_DIR, aSet + '.txt'), 'w')
    
    for entry in os.listdir(INpath):
        complexDIR = os.path.join(INpath, entry)
        if os.path.isdir(complexDIR):
            proteinIndex     = entry
            (PDBname, pKd) = libIO.readCSAR_KiFile(complexDIR)
            OUTLIST.write(PDBname + '\t' + str(pKd) + '\n')
            outputPDIR  = os.path.join(OUTpath, PDBname)
            print outputPDIR            
            if not os.path.exists(outputPDIR): # try to create the output dir for scores
                os.makedirs(outputPDIR)
            #OUTFILE.write('separateProteinLigand [DBPath, outPath, \"' + PDBname + '\", \"' + proteinIndex + '\", \"' + aSet + '\"];\n')
            molFILE = os.path.join(outputPDIR, PDBname + '_ligand.mol')
            sdfFILE = os.path.join(outputPDIR, PDBname + '_ligand.sdf')            
            OUTFILE.write('mv ' + molFILE + ' ' + sdfFILE + '\n')
            
    OUTLIST.close()
OUTFILE.close()

