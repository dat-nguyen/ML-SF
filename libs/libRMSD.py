__author__ = 'dat'

import subprocess
import os
import csv

def calcRMSD(refLigand, calcLigand):
    #FILE = open(refLigand+".tmp", "w")
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
                RMSDs[ligand] = calcRMSD(refLigand, calcLigand)
    return (RMSDs)

#
def writeRMSD2CSV(RMSDs, output):
    FILE = open(output, 'w')
    CSV = csv.writer(FILE, delimiter=',')
    # write the csv header
    CSV.writerow(["ID", "RMSDs"])

    for ligandID in RMSDs.keys():
        entry = [ligandID] + [RMSDs[ligandID]]
        CSV.writerow(entry)
    FILE.close()
