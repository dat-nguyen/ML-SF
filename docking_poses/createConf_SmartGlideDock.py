#!/home/dat/libs/miniconda3/bin/python3.5
# export PYTHONPATH=/mnt/zeus/dat/WORK/dev/ML-SF:$PYTHONPATH
"""
    create the smarter script for generate docking pose in glide
"""

from libs.libGlide import *

import subprocess

HOST_LIST   = ['athena', 'artemis', 'aphrodite', 'hades', 'eos', 'eros', 'hydra']
#HOST_LIST   = ['athena', 'artemis', 'aphrodite', 'poseidon', 'hades']
JOB_PER_HOST = 2

SSH_CMD     = "ssh -t -X "

#################################################################

def createSmartGlideDock(CASFyear, Core = True):
    proteinDir  = CASF_PATH[CASFyear]
    #indexFile   = CASF_CORE_INDEX[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    countProtein = 0
    countScript = 1

    # number of docking jobs per host calculated by total number of proteins divided by
    # number of total threads which could be submitted at once
    numDockingPerHost = (len(data.keys()) - countFinishDocking(CASFyear, glidescore="XP")) / (JOB_PER_HOST * len(HOST_LIST))

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'glide_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], countScript)), 'a')
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
                if not os.path.exists(os.path.join(scoreDir, proteinID, proteinID+'_XP_lib.maegz')):
                    countProtein = countProtein + 1 # count the number of ligands to be submitted
                    if countProtein > (numDockingPerHost * (countScript)):
                        countScript = countScript + 1
                        SHFILE  = open(os.path.join(OUTPUT_DIR, 'glide_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], countScript)), 'a')
                        SHFILE.write('export SCHRODINGER=/prog/schrodinger/2014u2\n')
                    # go to output dir for scores
                    scoreOutputDir = os.path.join(scoreDir, proteinID)
                    if not os.path.exists(scoreOutputDir): os.mkdir(scoreOutputDir)
                    SHFILE.write("cd {0}\n".format(scoreOutputDir))
                    # copy the ligand and protein in maegz format to destination
                    #SHFILE.write("cp {0} .\ncp {1} .\n".format(ligandFile, proteinFile))
                    # create grid config file and perform it
                    #SHFILE.write("$SCHRODINGER/run xglide.py -WAIT -NOJOBID {0}_grid.in\n".format(proteinID))
                    #createGridConf(scoreOutputDir, proteinID)
                    # only dock with SP score (faster)
                    createGlideConf(scoreOutputDir, proteinID, score="XP")
                    SHFILE.write("$SCHRODINGER/glide -WAIT -NOJOBID {0}_XP.in\n".format(proteinID))
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, proteinID))
                quit()
                # remove log and junk files
                #SHFILE.write("rm -rf *.restart *.out *.sdfgz *.maegz *.in *_workdir\n")
        else:
            print(os.path.join(proteinDir, proteinID) + " is not exist\n")
    print("Finish creating config for {0}, {1} proteins.".format(CASFyear, countProtein))
    return (countScript)

#################################################################
def submitJob2Shell(CASFyear, countScript):
    processes = set()
    max_processes = JOB_PER_HOST*len(HOST_LIST)

    cmd_list = []
    for i in range(1, countScript+1):
        cmd_list.append(' sh {2}glide_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], i, OUTPUT_DIR))

    for indexHost in range(0, len(HOST_LIST)):
        for index in range(0, JOB_PER_HOST):
            cmd = SSH_CMD + HOST_LIST[indexHost] + cmd_list[indexHost*JOB_PER_HOST+index]
            #print(cmd)
            processes.add(subprocess.Popen(cmd, shell=True))
            if len(processes) >= max_processes:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])

    # check if all the child processes were closed
    for p in processes:
        if p.poll() is None:
            p.wait()

CASFyear= '2007'
countScript = createSmartGlideDock(CASFyear)
submitJob2Shell(CASFyear, countScript)
