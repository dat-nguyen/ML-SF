import os

from libs import libIO
from libs import libRMSD
from libs.constConf import *
from libs.ioPDBbind import *
from libs import libGlide

#print(os.getcwd())
#os.chdir("/home/dat/WORK/output/test/")
#splitMol2(sys.argv[1])
#rmsds = libRMSD.calcRMSDPoses("ligand.mol2", "/home/dat/WORK/output/test/", prefix="_")

CASFyear = "2012"
proteinDir  = CASF_PATH[CASFyear]
indexFile   = CASF_REFINED_INDEX[CASFyear]
data1 = parse_index(proteinDir, indexFile)

CASFyear = "2013"
proteinDir  = CASF_PATH[CASFyear]
indexFile   = CASF_REFINED_INDEX[CASFyear]
data = parse_index(proteinDir, indexFile)

#newProt = libIO.createDisjointList(data.keys(), data1.keys())
#print(len(newProt), newProt)

def copyExistingDocking(CASFyear, CASFbased = "2012"):
    # base data for copying is the PDBbind 2012
    # init
    libGlide.convertPosesToMOL2(CASFbased, "SP")
    libGlide.convertPosesToMOL2(CASFbased, "XP")
    proteinDir  = CASF_PATH[CASFbased]
    indexFile   = CASF_REFINED_INDEX[CASFbased]
    data_base = parse_index(proteinDir, indexFile)

    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)

    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "glide")
    if not os.path.exists(scoreDir): os.mkdir(scoreDir)

    for proteinID in data.keys():
        # if the protein complex is in the base
        #  data, then copy instead of redock again
        if proteinID in data_base.keys():
            proteinDir = os.path.join(scoreDir, proteinID)
            if not os.path.exists(proteinDir): os.mkdir(proteinDir)
            glidescore = "XP"
            # only copying if the score dir does not exist in the new location
            if not os.path.exists(os.path.join(proteinDir, glidescore)):
                basePath = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFbased], "glide", proteinID)
                scorePath =os.path.join(basePath, glidescore)
                if os.path.exists(scorePath):
                    run_cmd = "cp -r {0} {1}\n".format(scorePath, proteinDir)
                    os.system(run_cmd)
                    scoreFile = os.path.join(basePath, '{0}_{1}_lib.maegz'.format(proteinID, glidescore))
                    run_cmd = "cp -r {0} {1}\n".format(scoreFile, proteinDir)
                    os.system(run_cmd)
                    print("copy {0} to {1}.".format(scorePath, proteinDir))
# \TODO: merge with glide
def copyExistingDockingPara(CASFyear, CASFbased = "2012"):
    # base data for copying is the PDBbind 2012
    proteinDir  = CASF_PATH[CASFbased]
    indexFile   = CASF_REFINED_INDEX[CASFbased]
    data_base = parse_index(proteinDir, indexFile)

    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)

    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "paradocks")
    if not os.path.exists(scoreDir): os.mkdir(scoreDir)

    for proteinID in data.keys():
        # if the protein complex is in the base
        #  data, then copy instead of redock again
        if proteinID in data_base.keys():
            basePath = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFbased], "paradocks", proteinID)
            if os.path.exists(basePath):
                run_cmd = "cp -r {0} {1}\n".format(basePath, scoreDir)
                os.system(run_cmd)
                print("copy {0} to {1}.".format(basePath, scoreDir))

#copyExistingDocking("2014", CASFbased = "2012")
#copyExistingDockingPara("2013", CASFbased = "2012")
#copyExistingDockingPara("2014", CASFbased = "2012")

#libGlide.checkGlideDock('2013', printing=False, glidescore="XP")
#libGlide.checkGlideDock('2013', printing=False, glidescore="SP")
#print(libGlide.countFinishDocking(CASFyear='2007', printing=True, dockingType="paradocks"))
#print(libGlide.countFinishDocking(CASFyear='2013', printing=True, dockingType="paradocks"))
#print(libGlide.countFinishDocking(CASFyear='2014', printing=False, dockingType="paradocks"))
