from libs.libGlide import *
from libs import libRMSD

PoseGeneratedMethods = ["gold", "glide"]
CASFyear = "2007"

proteinDir  = CASF_PATH[CASFyear]
indexFile   = CASF_REFINED_INDEX[CASFyear]

data = parse_index(proteinDir, indexFile)

# return list of protein ID with completed docking poses (means docking is successful)
def checkGoldPose(CASFyear, dockingMethod):
    poseDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "gold", dockingMethod)
    for proteinID in os.listdir(poseDir):
        RMSDdata    =  os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "_final", "{0}_RMSD.csv".format(proteinID))
        #print(poseDir)
        # find reference ligand location (mol2)
        refLigandPath = os.path.join(PDBBIND_DIR, CASF_VERSION[CASFyear], proteinID)
        refLigandFile = proteinID+"_complex_prep_lig.mol2"
        refLigand = os.path.join(refLigandPath, refLigandFile)
        RMSDs = libRMSD.calcRMSDPoses(refLigand, os.path.join(poseDir, proteinID), prefix = "gold_soln", suffix = ".mol2")
        print(RMSDs)




#for dockingMethod in GOLD_DOCKING_SCORE:

checkGoldPose(CASFyear, dockingMethod="goldscore")

#print(RMSD_DATA)