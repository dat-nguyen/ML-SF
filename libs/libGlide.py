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
def countFinishDocking(CASFyear, printing=False, dockingType = "glide", glidescore="SP"):
    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], dockingType)
    countProtein = 0
    for proteinID in os.listdir(scoreDir):
        if os.path.isdir(os.path.join(scoreDir, proteinID)):
            if dockingType == "glide":
                poseFile = "{0}_{1}_lib.maegz".format(proteinID, glidescore)
            elif dockingType == "paradocks":
                poseFile = "paradocks_prot1_lig1_mol1_soln1.mol2"
            poseFileFullPath = os.path.join(scoreDir, proteinID, poseFile)
            if os.path.exists(poseFileFullPath):
                countProtein = countProtein + 1
            if printing:
                if not os.path.exists(poseFileFullPath):
                    print(proteinID + " " + poseFile)
    return (countProtein)
#################################################################
def convertPosesToMOL2(CASFyear, glidescore="SP"):
    from libs import libIO
    import glob

    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "glide")

    for proteinID in os.listdir(scoreDir):
        proteinPath = os.path.join(scoreDir, proteinID)
        if os.path.isdir(proteinPath):
            poseFile = "{0}_{1}_lib".format(proteinID, glidescore)
            # only convert and calc the RMSD if the ligands (mol2 files) are not there
            if len( glob.glob(os.path.join(proteinPath, glidescore, "*.mol2")) ) == 0:
                if os.path.exists(os.path.join(proteinPath, poseFile+".maegz")):
                    posePath = os.path.join(proteinPath, glidescore)
                    if not os.path.exists(posePath): os.makedirs(posePath)
                    run_cmd = "/prog/schrodinger/2015u4/utilities/structconvert -imae {0}.maegz -omol2 {1}.mol2\n".\
                                format(os.path.join(proteinPath, poseFile), os.path.join(posePath, poseFile))
                    os.system(run_cmd)
                    # change location to the pose dir
                    os.chdir(posePath)
                    libIO.splitMol2(poseFile+".mol2")
                    # remove the multimol2 after splitting in multiple files
                    os.remove(poseFile+".mol2")
            else:
                pass # do nothing
    return (0) # for no error
#################################################################
# send number of scripts for CASFyear to all the host, using the shell and ssh
def submitJob2Shell(CASFyear, numScript, poseGenProg="glide"):
    # \TODO: the number of poses still need to be larger than the number of hosts, otherwise get a out of index error
    import subprocess
    processes = set()
    print("Max job per host: ", JOB_PER_HOST)
    max_processes = JOB_PER_HOST*len(HOST_LIST)

    cmd_list = []
    for i in range(1, numScript+1):
        cmd_list.append(' sh {2}{3}_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], i, OUTPUT_DIR, poseGenProg))
    for indexHost in range(0, len(HOST_LIST)):
        for index in range(0, JOB_PER_HOST):
            cmd = SSH_CMD + HOST_LIST[indexHost] + cmd_list[indexHost*JOB_PER_HOST+index]
            processes.add(subprocess.Popen(cmd, shell=True))
            if len(processes) >= max_processes:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])

    # check if all the child processes were closed
    for p in processes:
        if p.poll() is None:
            p.wait()
#################################################################
def checkExistingBashFile(CASFyear, prefix="glide"):
    import glob
    for bashfile in glob.glob(os.path.join(OUTPUT_DIR, "{0}_{1}*.sh".format(prefix, CASF_VERSION[CASFyear]))):
        os.remove(os.path.join(OUTPUT_DIR, bashfile))
        print("Deleted "+bashfile)
#################################################################
def checkGlideDock(CASFyear, printing=False, glidescore="SP"):
    proteinDir  = CASF_PATH[CASFyear]
    #indexFile   = CASF_CORE_INDEX[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    print("Total complexes for {0}: {1}".format(CASFyear, len(data.keys())))
    print("Finishing {0} protein complexes for {1}.".format(countFinishDocking(CASFyear, printing, glidescore=glidescore), CASFyear))
