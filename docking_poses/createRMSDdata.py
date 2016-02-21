#!/home/dat/libs/miniconda3/bin/python3.5
# export PYTHONPATH=/mnt/zeus/dat/WORK/dev/ML-SF:$PYTHONPATH

#######################################################################################
# create a pool of RMSD data from all kind of docking poses
# a RMSD pool for a protein will always be saved at _pool/{ProteinID}_RMSD.csv
# the csv file will contain the full path of the pose and its RMSD with the reference ligand
#######################################################################################
from libs.libGlide import *
from libs import libRMSD

import glob

DockingMethods = ["gold", "glide", "paradocks"]

#################################################################
def createRMSDdata(CASFyear, dockingMethod, scorFunc="para"):
    proteinDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], dockingMethod)
    if dockingMethod == "gold":
        proteinDir    = os.path.join(proteinDir, scorFunc)

    for proteinID in os.listdir(proteinDir):
        RMSDfile =  os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "_pool", "{0}_RMSD.csv".format(proteinID))
        # find reference ligand location (mol2)
        refLigandPath = os.path.join(PDBBIND_DIR, CASF_VERSION[CASFyear], proteinID)
        refLigandFile = proteinID+"_complex_prep_lig.mol2"
        refLigand = os.path.join(refLigandPath, refLigandFile)
        # only calculate the RMSD if its data still doesn't exist
        if (not os.path.exists(RMSDfile)) or (not libRMSD.IsPoseExistsFromCSV(RMSDfile, typeOfPose=scorFunc)):
            # spitting some outputs
            print("Calculating RMSDs poses for {0} {1} {2}...".format(proteinID, scorFunc, dockingMethod))
            poseDir = os.path.join(proteinDir, proteinID)
            suffix = ".mol2"
            if dockingMethod == "gold":
                prefix = "gold_soln"
            elif dockingMethod == "glide":
                poseDir = os.path.join(poseDir, scorFunc)
                #prefix = "_{0}".format(proteinID)
                prefix = ""
            elif dockingMethod == "paradocks":
                prefix = "paradocks"
            if os.path.exists(poseDir):
                RMSDs = libRMSD.calcRMSDPoses(refLigand, poseDir, prefix, suffix)
                libRMSD.writeRMSD2CSV(RMSDs, RMSDfile)
#################################################################
def preformRMSDcalculation(CASFyear):
    print("Creating RMSD data for {0}".format(CASFyear))
    convertPosesToMOL2(CASFyear, "SP")
    convertPosesToMOL2(CASFyear, "XP")
    for scorFunc in GLIDE_DOCKING_SCORE:
        createRMSDdata(CASFyear, dockingMethod="glide", scorFunc=scorFunc)
    for scorFunc in GOLD_DOCKING_SCORE:
        createRMSDdata(CASFyear, dockingMethod="gold", scorFunc=scorFunc)
    createRMSDdata(CASFyear, dockingMethod="paradocks")
#################################################################
def checkRMSDdata(CASFyear):
    RMSDpath =  os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "_pool")
    for RMSDfile in os.listdir(RMSDpath):
        for scorFunc in (GLIDE_DOCKING_SCORE + GOLD_DOCKING_SCORE):
            if not libRMSD.IsPoseExistsFromCSV(os.path.join(RMSDpath, RMSDfile), typeOfPose=scorFunc):
                print("In {0} doesn't exist {1}!".format(RMSDfile, scorFunc))
#################################################################
def filterDict(dict, minValue, maxValue):
    new_dict = {}
    for key in dict.keys():
        if (float(dict[key]) >= minValue) and (float(dict[key]) <= maxValue):
            new_dict[key] = dict[key]
    return (new_dict)
#################################################################
def samplingRMSDtoCluster(RMSDfile, numSamples = 100):
    import random
    RMSDs = libRMSD.readRMSDfromCSV(RMSDfile, WithRemovedLimit=10)
    samplesRMSD = {}
    totalSamplesPerCluster = int(numSamples / MAX_ANGSTROM)
    for value in range(MAX_ANGSTROM):
        filterRMSD = filterDict(RMSDs, minValue=value, maxValue=value+1)
        if len(filterRMSD.keys()) > totalSamplesPerCluster:
            samplesList = random.sample(filterRMSD.keys(), totalSamplesPerCluster)
            # create the new samplesRMSD
            randomRMSD = {}
            for key in samplesList:
                randomRMSD[key] = filterRMSD[key]
            filterRMSD = randomRMSD
        #print(filterRMSD)
        samplesRMSD.update(filterRMSD)
    return (samplesRMSD)
#################################################################
def samplingRMSDmixing(RMSDfile, numSamples = 100):
    import random
    RMSDs = libRMSD.readRMSDfromCSV(RMSDfile, WithRemovedLimit=10)
    if len(RMSDs.keys()) < numSamples:
        return (RMSDs)
    else:
        samplesList = random.sample(RMSDs.keys(), numSamples)
        # create the new samplesRMSD
        samplesRMSD = {}
        for key in samplesList:
            samplesRMSD[key] = RMSDs[key]
        return (samplesRMSD)
#################################################################
def samplingRMSDdata(CASFyear, numSamples = 100):
    RMSDpath =  os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "_pool")
    samplingPath =  os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "_sampling")
    for RMSDfile in os.listdir(RMSDpath):
        if os.path.getsize(os.path.join(RMSDpath, RMSDfile)) > 0:
            baseFileName, ext = os.path.splitext(RMSDfile)
            samplingFile = "{0}_sampling_clusters10.csv".format(baseFileName)
            samplesRMSD = samplingRMSDtoCluster(os.path.join(RMSDpath, RMSDfile), numSamples=numSamples)
            libRMSD.writeRMSD2CSV(samplesRMSD, os.path.join(samplingPath, samplingFile))
            samplingFile = "{0}_sampling_100.csv".format(baseFileName)
            samplesRMSD = samplingRMSDmixing(os.path.join(RMSDpath, RMSDfile), numSamples=numSamples)
            libRMSD.writeRMSD2CSV(samplesRMSD, os.path.join(samplingPath, samplingFile))
#################################################################
def checkStatsRMSDdata(CASFyear, samplingDir = "_sampling", samplingType = "sampling_clusters10"):
    samplingPath =  os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], samplingDir)
    numSamples = 0
    for RMSDfile in glob.glob(os.path.join(samplingPath, "*{0}.csv".format(samplingType))):
        # number of lines in a csv file is equivalent to number of samples for this protein
        numLines = sum(1 for line in open(RMSDfile))
        numSamples = numSamples + numLines
    return (numSamples)
#################################################################
#preformRMSDcalculation("2007")
#preformRMSDcalculation("2012")
#preformRMSDcalculation("2013")
#preformRMSDcalculation("2014")
#################################################################
#print(len(samplingRMSD("/home/dat/WORK/output/RMSD/v2007/_pool/5er1_RMSD.csv").keys()))
#samplingRMSDdata("2007")
#samplingRMSDdata("2012")
#samplingRMSDdata("2013")
#samplingRMSDdata("2014")
#################################################################
def printStatsRMSD(CASFyear):
    print(checkStatsRMSDdata(CASFyear, samplingType="sampling_clusters10"))
    print(checkStatsRMSDdata(CASFyear, samplingType="sampling_100"))
    print(checkStatsRMSDdata(CASFyear, samplingDir="_pool", samplingType="_RMSD"))
#################################################################
printStatsRMSD("2012")
printStatsRMSD("2013")
printStatsRMSD("2014")

