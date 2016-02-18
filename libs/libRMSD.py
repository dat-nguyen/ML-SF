__author__ = 'dat'

import subprocess
import os
import csv

# calc RMSD between reference ligand and target ligand, using rms_analysis tool
def calcRMSD(refLigand, calcLigand):
    run_cmd = "rms_analysis {0} {1}".format(refLigand, calcLigand)
    RMSDcalc = subprocess.Popen(run_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    RMSDresult = subprocess.Popen("tail -1".split(), stdin=RMSDcalc.stdout, stdout=subprocess.PIPE)
    RMSDcalc.stdout.close()
    RMSD = float(RMSDresult.communicate()[0].split()[0])
    return(RMSD)

# return a list of RMSDs for all poses in poseDir, pose files are assumed to start with prefix and end with suffix
def calcRMSDPoses(refLigand, poseDir, prefix = "gold_soln", suffix = ".mol2"):
    RMSDs = {}
    for ligand in os.listdir(poseDir):
        if ligand.startswith(prefix):
            if ligand.endswith(suffix):
                calcLigand = os.path.join(poseDir, ligand)
                RMSDs[os.path.join(poseDir, ligand)] = calcRMSD(refLigand, calcLigand)
    return (RMSDs)

#
def writeRMSD2CSV(RMSDs, output):
    FILE = open(output, 'a')
    CSV = csv.writer(FILE, delimiter=',')
    for ligandID in RMSDs.keys():
        entry = [ligandID] + [RMSDs[ligandID]]
        CSV.writerow(entry)
    FILE.close()

# WithRemovedLimit removes all the poses which excesses this value (in Anstrom)
def readRMSDfromCSV(input, WithRemovedLimit = 10):
    FILE = open(input, 'r')
    CSV = csv.reader(FILE, delimiter=',')
    RMSDs = {}
    for row in CSV:
        if float(row[1]) < WithRemovedLimit:
            RMSDs[row[0]] = row[1]
    FILE.close()
    return RMSDs

# return True if typeOfPose is found, False if not found anything
def IsPoseExistsFromCSV(CSVfile, typeOfPose):
    FILE = open(CSVfile, 'r')
    CSV = csv.reader(FILE, delimiter=',')
    for row in CSV:
        if str(row[0]).find(typeOfPose) > -1:
            FILE.close()
            return (True)
    return (False)
