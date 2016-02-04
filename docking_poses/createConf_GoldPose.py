from libs.constConf import *
from libs.libRMSD import *

SOURCE_CONF     = '/home/dat/WORK/docking_config/gold_pose.conf'
GAruns = 100
searchEff = 10

# create a config file to generate docking poses with gold, for any given protein and ligand, output to config dir and outputdir stores the docking results
def createGoldPose(path2protein, proteinID, path2ligand, ligandID, dockingMethod, outputDir, outputConfDir, GAruns = GAruns, searchEff = searchEff, prefix=""):
    outputConf  = 'gold_' + proteinID + '_' + ligandID + '_' + dockingMethod + '.conf'
    if not os.path.exists(outputConfDir): # try to create the dir path first
        os.makedirs(outputConfDir)
    if not os.path.exists(outputDir): # try to create the dir path first
        os.makedirs(outputDir)

    outputConf = os.path.join(outputConfDir, outputConf)
    OUTFILE = open(outputConf, 'w')
    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()
    # open file for reading and writing
    INFILE  = open(SOURCE_CONF, 'r')
    if (ligandID[-4:] != "mol2"):
        ligandID = ligandID + ".mol2"

    SHFILE  = open(os.path.join(OUTPUT_DIR, "RMSD", 'goldpose_run_'+prefix+dockingMethod+'.sh'), 'a')
    for line in INFILE:
        if line.find('cavity_file =') > -1:
            line = 'cavity_file = ' + os.path.join(path2ligand, ligandID) + '\n'
        elif line.find('ligand_data_file') > -1:
            line = 'ligand_data_file ' + os.path.join(path2ligand, ligandID) + ' ' + str(GAruns) + '\n'
        elif line.find('directory =') > -1:
            line = 'directory = ' + os.path.join(outputDir, proteinID) + '\n'
        elif line.find('protein_datafile =') > -1:
            line = 'protein_datafile = ' + os.path.join(path2protein, proteinID) + '_complex_prep_recep.pdb\n'

        elif line.find('gold_fitfunc_path =') > -1:
            line = 'gold_fitfunc_path = ' + dockingMethod + '\n'
        OUTFILE.write(line)

    # write sh script
    SHFILE.write('gold_auto ' + outputConf + '\n')
    # remove ranked files
    SHFILE.write('rm '+os.path.join(outputDir, proteinID)+'/ranked_*\n')
    #SHFILE.write('gold_cluster -l h_rt=20:00:00 ' + outputConf + " " + dockingMethod + '\n')

    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

def createGoldPosePDBbind(path2PDBbind, PDBbindSet, proteinID, dockingMethod, GAruns = GAruns, searchEff = searchEff):
    path2protein = os.path.join(path2PDBbind, PDBbindSet, proteinID)
    path2ligand = path2protein
    ligandID = proteinID + "_complex_prep_lig"
    outputDir       = os.path.join(OUTPUT_DIR, "RMSD", PDBbindSet, "gold", dockingMethod)
    outputConfDir   = os.path.join(OUTPUT_DIR, "RMSD", "conf", PDBbindSet, "gold", dockingMethod)
    createGoldPose(path2protein, proteinID, path2ligand, ligandID, dockingMethod, outputDir, outputConfDir, GAruns = GAruns, searchEff = searchEff, prefix = PDBbindSet)

def createGoldPosePDBbindFromSet(path2PDBbind, PDBbindSet, dockingMethod, GAruns = GAruns, searchEff = searchEff):
    path2protein = os.path.join(path2PDBbind, PDBbindSet)
    index = 0
    for proteinID in os.listdir(path2protein):
        if os.path.isdir(os.path.join(path2protein, proteinID)):
            index = index + 1 # count the number of ligands to be submitted
            #print(proteinID)
            if index > 10000: # can't submit too many jobs at once
                # add a sleep timer to the bash script
                SHFILE  = open(os.path.join(OUTPUT_DIR, 'gold_run_'+dockingMethod+'.sh'), 'a')
                SHFILE.write("sleep 2m\n")
                # reset the counter
                index = 0
            createGoldPosePDBbind(path2PDBbind, PDBbindSet, proteinID, dockingMethod, GAruns = GAruns, searchEff = searchEff)

def createGoldPosePDBbindAllMethods(PDBbindSet):
    for dockingMethod in GOLD_DOCKING_SCORE:
        createGoldPosePDBbindFromSet(PDBBIND_DIR, PDBbindSet, dockingMethod, GAruns = GAruns, searchEff = searchEff)

# check how many docking is success and print the failed
def checkSuccessDocking(outputDir):
    count = 0
    for proteinID in os.listdir(outputDir):
        if os.path.isdir(os.path.join(outputDir, proteinID)):
            match = [1 for x in os.listdir(os.path.join(outputDir, proteinID)) if x.find("gold_soln") > -1]
            if match != []:
                count = count + 1
            else:
                print(proteinID)
    return (count)


def main():
    PDBbindSet = "v2007"
    #createGoldPosePDBbindAllMethods(PDBbindSet)
    #createGoldPosePDBbindAllMethods("v2012-refined")
    #createGoldPosePDBbindAllMethods("v2013-refined")
    #createGoldPosePDBbindAllMethods("v2014-refined")

    #createGoldPose("/home/dat/WORK/DB/PDBbind/v2014-refined/3ejp/", "3ejp",
    #               "/home/dat/WORK/DB/PDBbind/v2014-refined/3ejp/", "3ejp_ligand.mol2", dockingMethod, "/home/dat/WORK/output/test/")
    #createGoldPosePDBbind(PDBBIND_DIR, PDBbindSet , "3ejp", dockingMethod)
    #calcLigand = "/home/dat/WORK/output/v2014-refined/plp/1hee/" + "gold_soln_1hee_ligand_m1_2.mol2"
    #refLigand = "/home/dat/WORK/DB/PDBbind/v2014-refined/1hee/" + "1hee_ligand.mol2"
    #calcRMSD(refLigand, calcLigand)
    #writeRMSD2CSV(calcRMSDPoses(refLigand, "/home/dat/WORK/output/v2014-refined/plp/1hee/"), "/home/dat/output.csv")
    #print(checkSuccessDocking("/home/dat/WORK/output/v2014-refined/goldscore/"))
main()