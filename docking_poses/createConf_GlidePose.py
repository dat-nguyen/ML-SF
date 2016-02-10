#!/home/dat/libs/miniconda3/bin/python3.5
# export PYTHONPATH=/mnt/zeus/dat/WORK/dev/ML-SF:$PYTHONPATH

"""
    create the script for docking in glide
"""

from libs.libGlide import *

#################################################################

def createGlideDock(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    #indexFile   = CASF_CORE_INDEX[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'glidedock_'+CASF_VERSION[CASFyear]+'.sh'), 'a')
    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "glide")

    # create scoreDir if not exists
    if not os.path.exists(scoreDir): os.mkdir(scoreDir)
    countProtein = 0
    countScript = 0
    for entry in data.keys():
        proteinIDDir = os.path.join(proteinDir, entry)
        if os.path.isdir(proteinIDDir):
        #if os.path.isdir(proteinIDDir) and (not entry in scoreOK):
            proteinFile = os.path.join(proteinDir, entry, entry + PROTEIN_SUFFIX + EXT_MAE)
            ligandFile  = os.path.join(proteinDir, entry, entry + LIGAND_SUFFIX + EXT_MAE)
            # only create config file if the ligand and the protein exist
            if os.path.exists(proteinFile) and  os.path.exists(ligandFile):
                countProtein = countProtein + 1 # count the number of ligands to be submitted
                if countProtein > 500: # can't submit too many jobs at once
                    # add a sleep timer to the bash script
                    countScript = countScript + 1
                    SHFILE  = open(os.path.join(OUTPUT_DIR, 'glidedock_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], countScript)), 'a')
                    SHFILE.write('export SCHRODINGER=/prog/schrodinger/2014u2\n')
                    # reset the counter
                    countProtein = 0
                # go to output dir for scores
                scoreOutputDir = os.path.join(scoreDir, entry)
                if not os.path.exists(scoreOutputDir): os.mkdir(scoreOutputDir)
                SHFILE.write("cd {0}\n".format(scoreOutputDir))
                # copy the ligand and protein in maegz format to destination
                SHFILE.write("cp {0} .\ncp {1} .\n".format(ligandFile, proteinFile))
                # create grid config file and perform it
                SHFILE.write("$SCHRODINGER/run xglide.py -WAIT -NOJOBID {0}_grid.in\n".format(entry))
                createGridConf(scoreOutputDir, entry)
                # only dock with SP score (faster)
                createGlideConf(scoreOutputDir, entry, score="XP")
                SHFILE.write("$SCHRODINGER/glide -WAIT -NOJOBID {0}_XP.in\n".format(entry))
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                quit()
            # remove log and junk files
            #SHFILE.write("rm -rf *.restart *.out *.sdfgz *.maegz *.in *_workdir\n")
            # move score files to parent dir
#            SHFILE.write("mv *.scor ..\n")
            # delete the empty folder
            #SHFILE.write("rm -rvf ../{0}\n".format(entry))
        else:
            print(os.path.join(proteinDir, entry) + " is not exist\n")
    print("Finish creating config for {0}, {1} proteins.".format(CASFyear, len(data.keys())))

def checkGlideDock(CASFyear, printing=False, glidescore="SP"):
    proteinDir  = CASF_PATH[CASFyear]
    #indexFile   = CASF_CORE_INDEX[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    print("Total complexes for {0}: {1}".format(CASFyear, len(data.keys())))
    print("Finishing {0} protein complexes for {1}.".format(countFinishDocking(CASFyear, printing, glidescore="XP"), CASFyear))

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

CASFyear = '2007'
checkGlideDock('2007', printing=True)
checkGlideDock('2012', printing=False)

# CAREFUL
#modifyGlideSetting('2007')
#modifyGlideSetting('2012')

#createGlideDock(CASFyear)
#createGlideDock('2012')
#createGlideScore('2013')
#createGlideScore('2014')

