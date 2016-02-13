#######################################################################################
# create a pool of RMSD data from all kind of docking poses
# a RMSD pool for a protein will always be saved at _pool/{ProteinID}_RMSD.csv
# the csv file will contain the full path of the pose and its RMSD with the reference ligand
#######################################################################################
from libs.libGlide import *
from libs import libRMSD

DockingMethods = ["gold", "glide", "paradocks"]

#
def createRMSDdata(CASFyear, dockingMethod, scoringFunc="para"):
    proteinDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], dockingMethod)
    if dockingMethod == "gold":
        proteinDir    = os.path.join(proteinDir, scoringFunc)

    for proteinID in os.listdir(proteinDir):
        RMSDfile =  os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "_pool", "{0}_RMSD.csv".format(proteinID))
        # find reference ligand location (mol2)
        refLigandPath = os.path.join(PDBBIND_DIR, CASF_VERSION[CASFyear], proteinID)
        refLigandFile = proteinID+"_complex_prep_lig.mol2"
        refLigand = os.path.join(refLigandPath, refLigandFile)
        # only calculate the RMSD if its data still doesn't exist
        if (not os.path.exists(RMSDfile)) or (not libRMSD.IsPoseExistsFromCSV(RMSDfile, typeOfPose=scoringFunc)):
            # spitting some outputs
            print("Calculating RMSDs poses for {0} {1} {2}...".format(proteinID, scoringFunc, dockingMethod))
            poseDir = os.path.join(proteinDir, proteinID)
            suffix = ".mol2"
            if dockingMethod == "gold":
                prefix = "gold_soln"
            elif dockingMethod == "glide":
                poseDir = os.path.join(poseDir, scoringFunc)
                prefix = "_{0}".format(proteinID)
            elif dockingMethod == "paradocks":
                prefix = "paradocks"
            if os.path.exists(poseDir):
                RMSDs = libRMSD.calcRMSDPoses(refLigand, poseDir, prefix, suffix)
                libRMSD.writeRMSD2CSV(RMSDs, RMSDfile)

def preformRMSDcalculation(CASFyear):
    for scorFunc in GLIDE_DOCKING_SCORE:
        createRMSDdata(CASFyear, dockingMethod="glide", scoringFunc=scorFunc)
    for scorFunc in GOLD_DOCKING_SCORE:
        createRMSDdata(CASFyear, dockingMethod="gold", scoringFunc=scorFunc)
    createRMSDdata(CASFyear, dockingMethod="paradocks")


CASFyear = "2007"
#createRMSDdata(CASFyear, dockingMethod="paradocks")
preformRMSDcalculation("2012")
#proteinDir  = CASF_PATH[CASFyear]
#indexFile   = CASF_REFINED_INDEX[CASFyear]

#data = parse_index(proteinDir, indexFile)
