import os

from libs.constConf import *

def createPrepProtein(PDBbindSet):
    path2protein = os.path.join(PDBBIND_DIR, PDBbindSet)
    SHFILE  = open(os.path.join(OUTPUT_DIR, 'prepwizard_'+PDBbindSet+'.sh'), 'w')
    #SHFILE.write("module load schrodinger/2014u2\n")
    print(len(os.listdir(path2protein)))
    for proteinID in os.listdir(path2protein):
        proteinIDDir = os.path.join(path2protein, proteinID)
        if os.path.isdir(proteinIDDir):
            # go directly to protein directory
            SHFILE.write("cd {0}\n".format(proteinIDDir))
            #line = "$SCHRODINGER/utilities/prepwizard -WAIT -NOJOBID {0}_complex.pdb {0}_complex_prep.maegz\n".format(proteinID)
            #SHFILE.write(line)
            # remove log and junk files
            #SHFILE.write("rm *.log *.mae \n")
            #SHFILE.write("$SCHRODINGER/utilities/structconvert -ipdb {0}_protein_prep.pdb -omol2 {0}_protein_prep.mol2\n".format(proteinID))
            SHFILE.write("$SCHRODINGER/run pv_convert.py -l -r {0}_complex_prep.maegz\n".format(proteinID))
            #SHFILE.write("$SCHRODINGER/utilities/mol2convert -imae {0}_complex_prep_lig.maegz -omol2 {0}_complex_prep_lig.mol2\n".format(proteinID))
            #SHFILE.write("$SCHRODINGER/utilities/pdbconvert -imae {0}_complex_prep_recep.maegz -opdb {0}_complex_prep_recep.pdb\n".format(proteinID))
            #SHFILE.write("rm {0}_complex_prep_*.maegz\n".format(proteinID))
    SHFILE.close()

def createPrepProtein_split(PDBbindSet, splitNum = 4, forPocket = ""):
    path2protein = os.path.join(PDBBIND_DIR, PDBbindSet)
    numOfFiles = len(os.listdir(path2protein)) / splitNum
    print(numOfFiles)
    proteinCounter = 0
    fileCounter = 1
    SHFILE  = open(os.path.join(OUTPUT_DIR, "prepwizard_{0}{2}_{1}.sh".format(PDBbindSet, fileCounter, forPocket)), 'w')
    SHFILE.write("module load schrodinger/2014u2\n")
    for proteinID in os.listdir(path2protein):
        proteinCounter = proteinCounter + 1
        proteinIDDir = os.path.join(path2protein, proteinID)
        if proteinCounter > numOfFiles:
            # reset the protein counter
            proteinCounter = 0
            SHFILE.close() # close the current sh file
            # open the next one
            fileCounter = fileCounter + 1
            SHFILE  = open(os.path.join(OUTPUT_DIR, "prepwizard_{0}{2}_{1}.sh".format(PDBbindSet, fileCounter, forPocket)), 'w')
            SHFILE.write("module load schrodinger/2014u2\n")
        if os.path.isdir(proteinIDDir):
            # go directly to protein directory
            SHFILE.write("cd {0}\n".format(proteinIDDir))
            # concat protein and ligand to pose viewer file (ligand must be at last pos)
            SHFILE.write("$SCHRODINGER/utilities/structcat -ipdb {0}_protein.pdb -isd {0}_ligand.sdf -omae {0}.maegz\n".format(proteinID))
            # merge to 1 complex file
            SHFILE.write("$SCHRODINGER/run pv_convert.py -m {0}.maegz\n".format(proteinID))
            # remove the pose viewer file
            SHFILE.write("rm {0}.maegz\n".format(proteinID))
            line = "$SCHRODINGER/utilities/prepwizard -WAIT -NOJOBID {0}_complex{1}.maegz {0}_complex{1}_prep.maegz\n".format(proteinID, forPocket)
            SHFILE.write(line)
            # remove log and junk files
            SHFILE.write("rm *.log *.mae \n")

    SHFILE.close()

def checkPrepProteinStatus(PDBbindSet, forPocket = ""):
    print(PDBbindSet)
    path2protein = os.path.join(PDBBIND_DIR, PDBbindSet)
    counter = 0
    SHFILE  = open(os.path.join(OUTPUT_DIR, "prepwizard_{0}{1}.sh".format(PDBbindSet, forPocket)), 'w')

    for proteinID in os.listdir(path2protein):
        proteinIDDir = os.path.join(path2protein, proteinID)
        if os.path.isdir(proteinIDDir):
            #if not os.path.exists(os.path.join(proteinIDDir, "{0}_complex{1}.pdb".format(proteinID, forPocket)) ):
            if not os.path.exists(os.path.join(proteinIDDir, "{0}_complex{1}_prep.maegz".format(proteinID, forPocket)) ):
                counter = counter + 1
                print(proteinID)
                SHFILE.write("cd {0}\n".format(proteinIDDir))
#                SHFILE.write("$SCHRODINGER/utilities/prepwizard -WAIT -NOJOBID {0}_complex{1}.pdb {0}_complex{1}_prep.maegz\n".format(proteinID, forPocket))
                SHFILE.write("$SCHRODINGER/utilities/structcat -ipdb {0}_protein.pdb -imol2 {0}_ligand.mol2 -omae {0}.maegz\n".format(proteinID))
                # merge to 1 complex file
                SHFILE.write("$SCHRODINGER/run pv_convert.py -m {0}.maegz\n".format(proteinID))
                # remove the pose viewer file
                SHFILE.write("rm {0}.maegz\n".format(proteinID))
                line = "$SCHRODINGER/utilities/prepwizard -WAIT -NOJOBID {0}_complex{1}.maegz {0}_complex{1}_prep.maegz\n".format(proteinID, forPocket)
                SHFILE.write(line)
                # remove log and junk files
                SHFILE.write("rm *.log *.mae \n")
    print(counter)
    SHFILE.close()


#createPrepProtein("v2007")
#createPrepProtein("v2012-refined")
#createPrepProtein("v2013-refined")
#createPrepProtein("v2014-refined")

#createPrepProtein_split("v2007", splitNum=2)
#createPrepProtein_split("v2012-refined", splitNum=4)
#createPrepProtein_split("v2013-refined", splitNum=4)
#createPrepProtein_split("v2014-refined", splitNum=4)

#createPrepProtein_split("v2007", splitNum=2, forPocket="_poc")

#checkPrepProteinStatus("v2007")
#checkPrepProteinStatus("v2012-refined")
#checkPrepProteinStatus("v2013-refined")
#checkPrepProteinStatus("v2014-refined")

