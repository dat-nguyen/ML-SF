#!/home/dat/libs/miniconda3/bin/python3.5
# export PYTHONPATH=/mnt/zeus/dat/WORK/dev/ML-SF:$PYTHONPATH
"""
    create the smarter script for generate docking pose for paradocks
"""

from libs.libGlide import *

SOURCE_CONF     = '/home/dat/WORK/docking_config/para_pose_PSO.xml'

#HOST_LIST   = ['athena', 'artemis', 'aphrodite', 'poseidon', 'hades']
#JOB_PER_HOST = 4
#################################################################
def createParaDocksConf(CASFyear, proteinID):
#   read the exemplary config and create the new config from given param
    outputConf  = proteinID + '_PSO.xml'
    outputPath = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "paradocks_pScore", proteinID)
    outputConf  = os.path.join(outputPath, outputConf)

    # create the dir path first if not exists
    if not os.path.exists(outputPath): os.makedirs(outputPath)
    OUTFILE = open(outputConf, 'w')

    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()

    # open file for reading and writing
    INFILE  = open(SOURCE_CONF, 'r')

    proteinDir  = CASF_PATH[CASFyear]
    proteinFile = os.path.join(proteinDir, proteinID, proteinID + PROTEIN_SUFFIX + EXT_MOL2)
    ligandFile = os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX + EXT_MOL2)

    for line in INFILE:
        if line.find('<Name>:2qci') > -1:
            line = '<Name>:' + proteinID + '_ligand</Name>\n'
        elif line.find('recep.mol2') > -1:
            line = '<File>' + proteinFile + '</File>\n'
        elif line.find('<ReferenceLigand') > -1:
            line = '<ReferenceLigand file=\"' + ligandFile + '\" proximity="7" />\n'
        elif line.find('lig.mol2</File>') > -1:
            line = '<File>' + ligandFile + '</File>\n'
        elif line.find('<OutputPath>') > -1: # <OutputPath>/home/dat/WORK</OutputPath>
            line = '<OutputPath>' + outputPath + '</OutputPath>\n'
        OUTFILE.write(line)

    INFILE.close()
    OUTFILE.close()
    return (outputConf)

#################################################################
def createParaDocksPose(CASFyear):
    checkExistingBashFile(CASFyear, prefix="para")
    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_REFINED_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    countProtein = 0
    numScript = 1

    # number of docking jobs per host calculated by total number of proteins divided by
    # number of total threads which could be submitted at once
    print(countFinishDocking(CASFyear, dockingType="paradocks"))
    numDockingPerHost = (len(data.keys()) - countFinishDocking(CASFyear, dockingType="paradocks_pScore") ) / (JOB_PER_HOST * len(HOST_LIST))
    SHFILE  = open(os.path.join(OUTPUT_DIR, 'para_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], numScript)), 'a')

    scoreDir    = os.path.join(OUTPUT_DIR, "RMSD", CASF_VERSION[CASFyear], "paradocks_pScore")
    # create scoreDir if not exists
    if not os.path.exists(scoreDir): os.mkdir(scoreDir)

    for proteinID in data.keys():
        proteinIDDir = os.path.join(proteinDir, proteinID)
        if os.path.isdir(proteinIDDir):
            proteinFile = os.path.join(proteinIDDir, proteinID + PROTEIN_SUFFIX)
            # smarter means if the docking solution is already there, then no need to redock again (save time)
            if not os.path.exists(os.path.join(scoreDir, proteinID, 'paradocks_prot1_lig1_mol1_soln1.mol2')):
                # convert PDB to MOL2
                cmd_convert = "/prog/schrodinger/2015u4/utilities/structconvert -imae {0}.maegz -omol2 {0}.mol2\n".format(proteinFile)
                # only convert when the protein in mol2 format not exist
                if not os.path.exists(proteinFile+EXT_MOL2): SHFILE.write(cmd_convert)

                countProtein = countProtein + 1 # count the number of ligands to be submitted
                if countProtein > (numDockingPerHost * (numScript)):
                    numScript = numScript + 1
                    SHFILE  = open(os.path.join(OUTPUT_DIR, 'para_{0}_{1}.sh'.format(CASF_VERSION[CASFyear], numScript)), 'a')
                outputConf = createParaDocksConf(CASFyear, proteinID)
                # move to the conf directory of the protein so paradocks will create mol2 to there (paradocks's bug)
                SHFILE.write('cd {0}\n'.format(os.path.join(scoreDir, proteinID)))
                SHFILE.write('/mnt/zeus/dat/WORK/dev/paradocks/build/bin/paradocks ' + outputConf + '\n')
                #SHFILE.write('/mnt/zeus/martin/WORK/final/paradocks_release/bin/paradocks ' + outputConf + '\n')

    SHFILE.close()

    print("Finish creating paradocks xml for {0}, {1} proteins.".format(CASFyear, countProtein))
    return (numScript)
#################################################################
#print(createParaDocksConf('2007', '2fwp'))
CASFyear = '2007'
numScript = createParaDocksPose(CASFyear)
submitJob2Shell(CASFyear, numScript, poseGenProg="para")
#createParaDocksScore('2012')
#createParaDocksScore('2013')
