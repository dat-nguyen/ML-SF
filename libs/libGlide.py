import os.path
# import constant
from libs.constConf import *
from libs.ioPDBbind import *

GRID_CONF   = '/home/dat/WORK/docking_config/grid.in'
SCORE_CONF  = '/home/dat/WORK/docking_config/glide_dock.in'
#################################################################
def createGridConf(outputDir, proteinID):
    outputConf  = "{0}_grid.in".format(proteinID)
    GRIDFILE   = open(os.path.join(outputDir, outputConf), 'w')
    # open file for reading and writing
    INFILE  = open(GRID_CONF, 'r')

    for line in INFILE:
        if line.find("RECEPTOR") > -1:
            line = "RECEPTOR {0}{1}.maegz\n".format(proteinID, PROTEIN_SUFFIX)
        elif line.find('LIGAND') > -1:
            line = "LIGAND {0}{1}.maegz,{0}{2}.maegz,REFPOSE\n".format(proteinID, LIGAND_SUFFIX, PROTEIN_SUFFIX)
        GRIDFILE.write(line)

    GRIDFILE.close()
    INFILE.close()
#################################################################
def createGlideConf(outputDir, proteinID, score):
    outputConf  = "{0}_{1}.in".format(proteinID, score)
    SCOREFILE   = open(os.path.join(outputDir, outputConf), 'w')
    # open file for reading and writing
    INFILE  = open(SCORE_CONF, 'r')

    for line in INFILE:
        if line.find("GRIDFILE") > -1:
            line = "GRIDFILE \"{0}_grid_workdir/{0}_grid__{0}{1}__grid.zip\"\n".format(proteinID, PROTEIN_SUFFIX)
        elif line.find("LIGANDFILE ") > -1:
            line = "LIGANDFILE \"{0}{1}.maegz\"\n".format(proteinID, LIGAND_SUFFIX)
        SCOREFILE.write(line)
    if score=="XP":
        SCOREFILE.write("PRECISION \"XP\"\n")

    SCOREFILE.close()
    INFILE.close()
#################################################################
def countFinishDocking(CASFyear, printing=False):
    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "glide")
    countProtein = 0
    for proteinID in os.listdir(scoreDir):
        if os.path.isdir(os.path.join(scoreDir, proteinID)):
            if os.path.exists(os.path.join(scoreDir, proteinID, proteinID+'_SP_lib.maegz')):
                countProtein = countProtein + 1
            if printing:
                if not os.path.exists(os.path.join(scoreDir, proteinID, proteinID+'_SP_lib.maegz')):
                    print(proteinID+'_SP_lib.maegz')
    return (countProtein)