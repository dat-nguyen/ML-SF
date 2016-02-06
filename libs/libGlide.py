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
def countFinishDocking(CASFyear, printing=False, glidescore="SP"):
    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "glide")
    countProtein = 0
    for proteinID in os.listdir(scoreDir):
        if os.path.isdir(os.path.join(scoreDir, proteinID)):
            poseFile = "{0}_{1}_lib.maegz".format(proteinID, glidescore)
            poseFileFullPath = os.path.join(scoreDir, proteinID, poseFile)
            if os.path.exists(poseFileFullPath):
                countProtein = countProtein + 1
            if printing:
                if not os.path.exists(poseFileFullPath):
                    print(poseFile)
    return (countProtein)
#################################################################
def convertPosesToMOL2(CASFyear, glidescore="SP"):
    from libs import libIO

    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "glide")

    for proteinID in os.listdir(scoreDir):
        proteinPath = os.path.join(scoreDir, proteinID)
        if os.path.isdir(proteinPath):
            poseFile = "{0}_{1}_lib".format(proteinID, glidescore)
            if os.path.exists(os.path.join(proteinPath, poseFile+".maegz")):
                posePath = os.path.join(proteinPath, glidescore)
                if not os.path.exists(posePath):
                    os.makedirs(posePath)
                run_cmd = "/prog/schrodinger/2015u4/utilities/structconvert -imae {0}.maegz -omol2 {1}.mol2\n".\
                            format(os.path.join(proteinPath, poseFile), os.path.join(posePath, poseFile))
                os.system(run_cmd)
                # change location to the pose dir
                os.chdir(posePath)
                libIO.splitMol2(poseFile+".mol2")
                # remove the multimol2 after splitting in multiple files
                os.remove(poseFile+".mol2")

    return (0) # for no error