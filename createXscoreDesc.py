import os
import csv

from libs.constConf import *

XSCORE_HEADER = ["ID", "MW", "LogP", "VDW", "HB", "HP", "HM", "HS", "RT"]
SOURCE_CONF   = '/home/dat/WORK/docking_config/xscore.conf'
dockingMethods = ["asp", "plp", "chemscore", "goldscore", "SP", "XP"]

# read desc from xscore log file, includes VDW, HB, etc.
def readFromLog(path, ligandID):
    file = os.path.join(path, ligandID + '.log')
    if not os.path.exists(file):
        print("File {0} does not exist.".format(file))
        return []
    else:
        LOGFILE = open(file, 'r')

    for line in LOGFILE:
        if (line.split() != []):
            if (line.split()[0]) == "Total":
                return (line.split()[1:7])

# read desc from xscore table file, includes Mol Weight and LogP of ligand
def readFromTable(path, ligandID):
    file = os.path.join(path, ligandID + '.table')
    if not os.path.exists(file):
        print("File {0} does not exist.".format(file))
        return []
    else:
        LOGFILE = open(file, 'r')
    line = LOGFILE.readline() # skip the first line
    line = LOGFILE.readline()
    return (line.split()[2:4])

# write xscore desc from all desc files in path, write to output with csv format
# a xscore desc comes in a paar, a .log and .table file.
def writeXScoreDesc(path, output):
    FILE = open(output, 'w')
    CSV = csv.writer(FILE, delimiter=',')
    # write the csv header
    CSV.writerow(XSCORE_HEADER)

    ligandList = [x for x in os.listdir(path) if x.endswith(".log")]
    for ligandID in ligandList:
        ligandID = ligandID[:-4] # remove the .log ending (4 characters)
        if (ligandID[-4:] == "mol2"):
            # remove the .mol2 ending (5 characters)
            ID = ligandID[:-5]
        else:
            ID = ligandID
        desc = [ID] + readFromTable(path, ligandID) + readFromLog(path, ligandID)
        CSV.writerow(desc)
    FILE.close()

# create xscore config file for a protein and a ligand, output config file will be written to outputDir
def createXScoreConf(path2protein, proteinID, path2ligand, ligandID, outputDir, outputConfDir):
    if not os.path.exists(outputConfDir): # try to create the dir path first
        os.makedirs(outputConfDir)
    if not os.path.exists(outputDir): # try to create the dir path first
        os.makedirs(outputDir)

#   read the exemplary config and create the new config from given param
    ligandID_fix = ligandID.replace('|','__')
    outputConf  = 'xscore_' + ligandID_fix + '.conf'

    confPath = os.path.join(outputConfDir, outputConf)
    OUTFILE = open(confPath, 'w')

    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()

    # open file for reading and writing
    INFILE  = open(SOURCE_CONF, 'r')
    SHFILE  = open(os.path.join(OUTPUT_DIR, 'xscore_run_'+proteinID+'.sh'), 'a')

    if (ligandID[-4:] != "mol2"):
        ligandID = ligandID + ".mol2"
    for line in INFILE:
        if line.find('RECEPTOR_PDB_FILE ') > -1:
            line = 'RECEPTOR_PDB_FILE ' + os.path.join(path2protein, proteinID + '.pdb\n')
        elif line.find('REFERENCE_MOL2_FILE ') > -1:
            line = 'REFERENCE_MOL2_FILE ' + os.path.join(path2ligand, ligandID + '\n')
        elif line.find('LIGAND_MOL2_FILE ') > -1:
            line = 'LIGAND_MOL2_FILE ' + os.path.join(path2ligand, ligandID + '\n')
        elif line.find('OUTPUT_TABLE_FILE ') > -1:
            line = 'OUTPUT_TABLE_FILE ' + os.path.join(outputDir, ligandID + '.table\n')
        elif line.find('OUTPUT_LOG_FILE ') > -1:
            line = 'OUTPUT_LOG_FILE ' + os.path.join(outputDir, ligandID + '.log\n')
        OUTFILE.write(line)

    # write sh script
    SHFILE.write('xscore ' + confPath + '\n')

    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

def listFiles(path, pattern):
    if not os.path.exists(path):
        print(path + " not exists")
        return []
    match = [x for x in os.listdir(path) if x.find(pattern) > -1]
    return (match)


def createXScoreConfForDockingPoses(proteinStatus, proteinDB, DBver, proteinID, dockingMethod):
#   read the exemplary config and create the new config from given param

    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'xscore_run_'+DBver+"_RMSD_"+dockingMethod+'.sh'), 'a')


    pose_path = os.path.join(OUTPUT_DIR, DBver, dockingMethod, proteinID)
    outputPath = os.path.join(OUTPUT_DIR, 'conf', "RMSD", DBver, 'xscore', method)
    if not os.path.exists(outputPath): # try to create the dir path first
        os.makedirs(outputPath)

    outputScore = os.path.join(OUTPUT_DIR, "RMSD", DBver, 'xscore', method)
    if not os.path.exists(outputScore): # try to create the output dir for scores
        os.makedirs(outputScore)

    lig_pattern = "gold_soln"
    for pose in listFiles(pose_path, lig_pattern):

        outputConf  = 'xscore_' + '_' + pose + '_' + dockingMethod + '.conf'
        outputConf  = os.path.join(outputPath, outputConf)

        OUTFILE = open(outputConf, 'w')

        lig_path = os.path.join(OUTPUT_DIR, DBver, dockingMethod, proteinID, pose)
        # open file for reading and writing
        INFILE  = open(SOURCE_CONF, 'r')

        for line in INFILE:
            if line.find('RECEPTOR_PDB_FILE ') > -1:
                line = 'RECEPTOR_PDB_FILE ' + os.path.join(proteinDir, proteinID, proteinID + lPROTEIN_SUFFIX[proteinStatus] + '\n')
            elif line.find('REFERENCE_MOL2_FILE ') > -1:
                line = 'REFERENCE_MOL2_FILE ' + os.path.join(lig_path+'\n')
            elif line.find('LIGAND_MOL2_FILE ') > -1:
                line = 'LIGAND_MOL2_FILE ' + os.path.join(lig_path+'\n')
            elif line.find('OUTPUT_TABLE_FILE ') > -1:
                line = 'OUTPUT_TABLE_FILE ' + os.path.join(outputScore, pose+'_'+method+'.table\n')
            elif line.find('OUTPUT_LOG_FILE ') > -1:
                line = 'OUTPUT_LOG_FILE ' + os.path.join(outputScore, pose+'_'+method+'.log\n')
            OUTFILE.write(line)

        # write sh script
        SHFILE.write('xscore ' + outputConf + '\n')
        OUTFILE.close()
        INFILE.close()

    SHFILE.close()

# end createXScoreConfForDockingPoses

def main_old():
    for entry in proteinDict.keys():
        print(entry)
        if os.path.isdir(os.path.join(proteinDir, entry)):
            proteinFile = entry + PROTEIN_SUFFIX
            for method in dockingMethods:
                #ligandFile  = entry + LIGAND_SUFFIX
                if os.path.exists(os.path.join(proteinDir, entry, proteinFile)):# and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
                    # only create config file if the ligand and the protein exist
                    #createGoldConf(lPROTEIN_STATUS[0], lPROTEIN_DB[0], lPROTEIN_DB_VER[0], entry, lSCORE[0])
                    createXScoreConfForDockingPoses(proteinStatus, lPROTEIN_DB[0], lPROTEIN_DB_VER[i], entry, method)
                else:
                    print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                    quit()

def createXScoreConfFromDir(path2protein, proteinID, path2ligand, outputDir, outputConfDir):
    for ligandID in os.listdir(path2ligand):
        createXScoreConf(path2protein, proteinID, path2ligand, ligandID, outputDir, outputConfDir)

def createConfDUD():

    createXScoreConfFromDir("/home/dat/WORK/DB/DUD-E/docked_by_Rognan/FGFR1/", "protein_prep",
                     "/home/dat/WORK/DB/DUD-E/docked_by_Rognan/FGFR1/docked",
                     "/home/dat/WORK/output/DUD-E/FGFR1/",
                     "/home/dat/WORK/output/conf/DUD-E/FGFR1/")

def createConfForDockingSolution(path2protein, proteinID, path2ligand, outputDir, outputConfDir, dockingMethods):
    for method in dockingMethods:
        createXScoreConfFromDir(path2protein, proteinID, path2ligand+method, outputDir+method, outputConfDir+method)

def createConfCSAR2013():
    createConfForDockingSolution("/home/dat/WORK/DB/CSAR/2013/cs/", "DIG10.2_CS337_B_6_min_prep",
                         "/home/dat/WORK/DB/CSAR/2013/cs/cs-confgen_all/",
                         "/home/dat/WORK/output/cs-confgen/xscore/",
                         "/home/dat/WORK/output/conf/cs-confgen/xscore/", dockingMethods)

def writeXScore():
    #writeXScoreDesc("/home/dat/WORK/output/DUD-E/ADA", "/home/dat/WORK/DB/DESCRIPTORS/DUD-E_ADA_xscore.csv")
    #writeXScoreDesc("/home/dat/WORK/output/DUD-E/FGFR1", "/home/dat/WORK/DB/DESCRIPTORS/DUD-E/DUD-E_FGFR1_xscore.csv")
            #writeXScoreDesc("/home/dat/WORK/output/DUD-E/RENI", "/home/dat/WORK/DB/DESCRIPTORS/DUD-E/DUD-E_RENI_xscore.csv")
    #writeXScoreDesc("/home/dat/WORK/output/v2014-refined/xscore/", "/home/dat/WORK/DB/DESCRIPTORS/2014_xscore.csv")
    #writeXScoreDesc("/home/dat/WORK/output/v2014-refined/xscore/", "/home/dat/WORK/DB/DESCRIPTORS/2014_xscore.csv")
    writeXScoreDesc("/home/dat/WORK/output/PDBbind/v2007/xscore/", "/home/dat/WORK/DB/DESCRIPTORS/CASF/CASF07_refined_xscore.csv")
    writeXScoreDesc("/home/dat/WORK/output/PDBbind/v2012-refined/xscore/", "/home/dat/WORK/DB/DESCRIPTORS/CASF/CASF12_refined_xscore.csv")
    writeXScoreDesc("/home/dat/WORK/output/PDBbind/v2013-refined/xscore/", "/home/dat/WORK/DB/DESCRIPTORS/CASF/CASF13_refined_xscore.csv")
    writeXScoreDesc("/home/dat/WORK/output/PDBbind/v2014-refined/xscore/", "/home/dat/WORK/DB/DESCRIPTORS/CASF/CASF14_refined_xscore.csv")
#    for method in dockingMethods:
#        writeXScoreDesc("/home/dat/WORK/output/RMSD/v2014-refined/xscore/"+method, "/home/dat/WORK/DB/DESCRIPTORS/CASF14_refined_xscore_"+method+".csv")
#        writeXScoreDesc("/home/dat/WORK/output/cs-confgen/xscore/"+method, "/home/dat/WORK/DB/DESCRIPTORS/DIG10.2/confgen/DIG10.2_xscore_"+method+".csv")
#createConfCSAR2013()

def main():
#    createXScoreConfFromDir("/home/dat/WORK/DB/DUD-E/docked_by_Rognan/FGFR1/", "protein_prep",
#                     "/home/dat/WORK/DB/DUD-E/docked_by_Rognan/FGFR1/docked",
#                     "/home/dat/WORK/output/DUD-E/FGFR1/",
#                     "/home/dat/WORK/output/conf/DUD-E/FGFR1/")

    writeXScore()
main()

