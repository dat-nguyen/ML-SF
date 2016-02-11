#!/usr/bin/python

"""
    create the script for docking in glide
"""

import os.path

from libs.ioPDBbind import *
# import constant
from libs.constConf import *
from libs.libGlide import *

GRID_CONF   = '/home/dat/WORK/docking_config/grid.in'
SCORE_CONF  = '/home/dat/WORK/docking_config/glide_inplace.in'

#################################################################

def createGlideScore(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_CORE_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'glide_run_'+CASF_VERSION[CASFyear]+'.sh'), 'a')
    scoreDir    = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], "glide")

    #scorePath   = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], "glidescore")
    ## what does this code snippet ?
    #scoreOK = {}
    #for ID in os.listdir(scorePath):
    #    ID = ID.split('_')[0]
    #    scoreOK[ID] = "OK"

    if not os.path.exists(scoreDir): os.mkdir(scoreDir)
    for entry in data.keys():
        proteinIDDir = os.path.join(proteinDir, entry)
        if os.path.isdir(proteinIDDir):
        #if os.path.isdir(proteinIDDir) and (not entry in scoreOK):
            proteinFile = os.path.join(proteinDir, entry, entry + PROTEIN_SUFFIX + EXT_MAE)
            ligandFile  = os.path.join(proteinDir, entry, entry + LIGAND_SUFFIX + EXT_MAE)
            if os.path.exists(proteinFile) and  os.path.exists(ligandFile):
            # only create config file if the ligand and the protein exist
                # go to output dir for scores
                scoreOutputDir = os.path.join(scoreDir, entry)
                if not os.path.exists(scoreOutputDir): os.mkdir(scoreOutputDir)
                SHFILE.write("cd {0}\n".format(scoreOutputDir))
                # copy the ligand and protein in maegz format to destination
                SHFILE.write("cp {0} .\ncp {1} .\n".format(ligandFile, proteinFile))
                # convert sdf ligand file to maegz
                #SHFILE.write("$SCHRODINGER/utilities/sdconvert -isd {0} -omae {1}{2}.maegz\n".format(ligandFile, entry, LIGAND_SUFFIX))
                # convert mol2 ligand file to maegz
                #SHFILE.write("$SCHRODINGER/utilities/mol2convert -imol2 {0} -omae {1}{2}.maegz\n".format(ligandFile, entry, LIGAND_SUFFIX))
                # convert pdb protein file to maegz
                #SHFILE.write("$SCHRODINGER/utilities/pdbconvert -ipdb {0} -omae {1}{2}.maegz\n".format(proteinFile, entry, PROTEIN_SUFFIX))
                #
                # create grid config file and perform it
                SHFILE.write("$SCHRODINGER/run xglide.py -WAIT -NOJOBID {0}_grid.in\n".format(entry))
                createGridConf(scoreOutputDir, entry)
                for score in ["SP", "XP"]:
                    createGlideConf(scoreOutputDir, entry, score)
                SHFILE.write("$SCHRODINGER/glide -WAIT -NOJOBID {0}_SP.in\n".format(entry))
                SHFILE.write("$SCHRODINGER/glide -WAIT -NOJOBID {0}_XP.in\n".format(entry))
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                quit()
            # remove log and junk files
            #SHFILE.write("rm -rf *.restart *.out *.sdfgz *.maegz *.in *_workdir\n")
            # move score files to parent dir
            SHFILE.write("mv *.scor ..\n")
            # delete the empty folder
            #SHFILE.write("rm -rvf ../{0}\n".format(entry))
        else:
            print(os.path.join(proteinDir, entry) + " is not exist\n")
    print("Finish creating config for {0}, {1} proteins.".format(CASFyear, len(data.keys())))
# very greedy, CAREFUL, always remove the first line in the setting file
# \TODO: obsolete for now
def modifyGlideSetting(CASFyear):
    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "glide")
    for proteinID in os.listdir(scoreDir):
        if os.path.isdir(os.path.join(scoreDir, proteinID)):
            settingFile = os.path.join(scoreDir, proteinID, proteinID+"_SP.in")
            bashCommand = "sed -i '1d' "+settingFile
#            print(bashCommand)
            os.system(bashCommand)
    print("Finish.")

##### obsolete #####
def moveGlideScore(CASFyear):
    SHFILE  = open(os.path.join(OUTPUT_DIR, 'glide_move_'+CASF_VERSION[CASFyear]+'.sh'), 'a')
    scoreDir    = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], "glide")

    for entry in os.listdir(scoreDir):
        scoreIDDir = os.path.join(scoreDir, entry)
        if os.path.isdir(scoreIDDir):
            SHFILE.write("cd {0}\n".format(scoreIDDir))
            SHFILE.write("mv *.rept ..\n")

    SHFILE.close()

def checkGlideScore(CASFyear):
    scoreDir    = os.path.join(OUTPUT_DIR, "PDBbind", CASF_VERSION[CASFyear], "glide")
    for proteinID in os.listdir(scoreDir):
        if os.path.isdir(os.path.join(scoreDir, proteinID)):
            #if not os.path.exists(os.path.join(proteinIDDir, proteinID+'_protein_prep.pdb')):
            if not os.path.exists(os.path.join(scoreDir, proteinID+'_XP.scor')):
                print(proteinID+'_XP.scor')
            if not os.path.exists(os.path.join(scoreDir, proteinID+'_SP.scor')):
                print(proteinID+'_SP.scor')

CASFyear = '2007'
#checkGlideScore('2007')
#checkGlideScore('2013')
#moveGlideScore('2012')
#moveGlideScore('2013')
#createGlideScore(CASFyear)
createGlideScore('2013')
createGlideScore('2014')

