#!/home/dat/libs/miniconda3/bin/python3.5
# export PYTHONPATH=/mnt/zeus/dat/WORK/dev/ML-SF:$PYTHONPATH
"""
    create the smarter script for generate docking pose in glide
"""

from libs.libGlide import *

#################################################################
def createSmartGlideDock(CASFyear, glidescore="SP"):
    checkExistingBashFile(CASFyear)
    proteinDir  = CASF_PATH[CASFyear]
    #indexFile   = CASF_CORE_INDEX[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    countProtein = 0
    # number of total bash scripts will be created
    numScript = 1

    # number of docking jobs per host calculated by total number of proteins divided by
    # number of total threads which could be submitted at once
    numDockingPerHost = (len(data.keys()) - countFinishDocking(CASFyear, glidescore=glidescore)) / (JOB_PER_HOST * len(HOST_LIST))

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'glide_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], numScript)), 'a')
    SHFILE.write('export SCHRODINGER=/prog/schrodinger/2014u2\n')

    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "glide")
    # create scoreDir if not exists
    if not os.path.exists(scoreDir): os.mkdir(scoreDir)

    for proteinID in data.keys():
        proteinIDDir = os.path.join(proteinDir, proteinID)
        if os.path.isdir(proteinIDDir):
        #if os.path.isdir(proteinIDDir) and (not proteinID in scoreOK):
            proteinFile = os.path.join(proteinDir, proteinID, proteinID + PROTEIN_SUFFIX + EXT_MAE)
            ligandFile  = os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX + EXT_MAE)
            # only create config file if the ligand and the protein exist
            if os.path.exists(proteinFile) and  os.path.exists(ligandFile):
                # smarter means if the docking solution is already there, then no need to redock again (save time)
                if not os.path.exists(os.path.join(scoreDir, proteinID, '{0}_{1}_lib.maegz'.format(proteinID, glidescore))):
                    countProtein = countProtein + 1 # count the number of ligands to be submitted
                    if countProtein > (numDockingPerHost * (numScript)):
                        numScript = numScript + 1
                        SHFILE  = open(os.path.join(OUTPUT_DIR, 'glide_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], numScript)), 'a')
                        SHFILE.write('export SCHRODINGER=/prog/schrodinger/2014u2\n')
                    # go to output dir for scores
                    scoreOutputDir = os.path.join(scoreDir, proteinID)
                    if not os.path.exists(scoreOutputDir): os.mkdir(scoreOutputDir)
                    SHFILE.write("cd {0}\n".format(scoreOutputDir))
                    # copy the ligand and protein in maegz format to destination
                    SHFILE.write("cp {0} .\ncp {1} .\n".format(ligandFile, proteinFile))
                    # create grid config file and perform it
                    SHFILE.write("$SCHRODINGER/run xglide.py -WAIT -NOJOBID {0}_grid.in\n".format(proteinID))
                    createGridConf(scoreOutputDir, proteinID)
                    # create score file
                    createGlideConf(scoreOutputDir, proteinID, score=glidescore)
                    SHFILE.write("$SCHRODINGER/glide -WAIT -NOJOBID {0}_{1}.in\n".format(proteinID, glidescore))
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, proteinID))
                quit()
                # remove log and junk files
                #SHFILE.write("rm -rf *.restart *.out *.sdfgz *.maegz *.in *_workdir\n")
        else:
            print(os.path.join(proteinDir, proteinID) + " is not exist\n")
    print("Finish creating config for {0}, {1} proteins.".format(CASFyear, countProtein))
    return (numScript)
#################################################################

CASFyear= '2012'
numScript = createSmartGlideDock(CASFyear, glidescore="SP")
submitJob2Shell(CASFyear, numScript, poseGenProg="glide")
