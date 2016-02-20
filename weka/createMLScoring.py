#!/home/dat/libs/miniconda3/bin/python3.5
# export PYTHONPATH=/mnt/zeus/dat/WORK/dev/ML-SF:$PYTHONPATH

__author__ = 'dat'

'''
    create ML training model in weka

'''

import os.path
import subprocess, glob

trainingPath    = "/home/dat/WORK/arff/"
testPath        = "/home/dat/WORK/arff/"

#resultPath        = "/home/dat/WORK/arff/"
resultPath      = "/home/dat/WORK/RESULTS/2016-02-23/"

PREFIX_JAVA     = "java -Xmx30000M "
THREADNUM       = 8
ITERATION       = 100
CLASSIFI        = "-t train.arff -T test.arff -c 1 -no-cv -o -classifications "
OUTPUT_CSV      = "\"weka.classifiers.evaluation.output.prediction.CSV\""
FILTER_PCA      = "\"weka.filters.unsupervised.attribute.PrincipalComponents -R 1.0 -A 5 -M -1\""
RANDOM_COMMITTEE = "-W weka.classifiers.meta.RandomCommittee -- -S 6 -num-slots {0} -I 10 ".format(THREADNUM)

cmdRemove    = PREFIX_JAVA + "weka.filters.unsupervised.attribute.Remove -R first -i {0} -o {1}\n"
cmdReplace   = PREFIX_JAVA + "weka.filters.unsupervised.attribute.RenameAttribute -find \"scores\" -replace \"pKd.pKi\" -i {0} -o {1}\n"

shortName = {"RotationForest"   : "RoF",
             "Bagging"          : "Bagging",
             "RandomSubSpace"   : "RandSS",
             "RandomForest"     : "RF"}

metaClassifier  = {"RotationForest" : "weka.classifiers.meta.RotationForest ",
                   "Bagging"        : "weka.classifiers.meta.Bagging ",
                   "RandomSubSpace" : "weka.classifiers.meta.RandomSubSpace ",
                   "RandomForest"   : "weka.classifiers.trees.RandomForest "}

metaClassifierSetting = {"RotationForest"   : " -G 3 -H 3 -P 50 -F " + FILTER_PCA + " -S 8 -num-slots {0} -I {1} ".format(THREADNUM, ITERATION),
                         "Bagging"          : " -P 100 -S 1 -num-slots {0} -I {1} ".format(THREADNUM, ITERATION),
                         "RandomSubSpace"   : " -P 0.5 -S 1 -num-slots {0} -I {1} ".format(THREADNUM, ITERATION),
                         "RandomForest"     : " -I 500 -K 0 -S 1 -num-slots {0} ".format(THREADNUM)}
baseClassifier  = {"RoT"  : "-W weka.classifiers.trees.RandomTree -- -K 0 -M 1.0 -V 0.001 -S 66 ",
                   "REPT" : "-W weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 88 -L -1 -P -I 0.0 "}
# COMMAND = PREFIX_JAVA + metaClassifier + CLASSIFI + OUTPUT_CSV + metaClassifierSetting + RANDOM_COMMITTEE + baseClassifier

prefixTrainModel     = "-t {0} -d "
suffixTrainModel     = " -c 1 -no-cv "

#CMD_TRAIN = PREFIX_JAVA + metaClassifier + prefixTrainModel + dumpModel + suffixTrainModel + metaClassifierSetting + RANDOM_COMMITTEE + baseClassifier + " > dummy_stats.txt \n"
                #cmdDumpModel1 + dumpModel + cmdDumpModel2 + postCmdRoF + postCmdRoF_Methods[i] + " > dummy_stats.txt \n"

prefixTestModel     = " -l "
suffixTestModel     = " -T {0} -c 1 -v -o -classifications " + OUTPUT_CSV + " "

#CMD_TEST = PREFIX_JAVA + metaClassifier + prefixTestModel + dumpModel + suffixTestModel + " > " + resultName + "\n"
#            line = cmdTestModel1 + dumpModel + cmdTestModel2 + " > " + resultName + "\n"

#postCmdRoF = "\"weka.filters.unsupervised.attribute.PrincipalComponents -R 1.0 -A 5 -M -1\" -S 1 -num-slots 8 -I 100 " #\
#postCmdRoFwithRC = "\"weka.filters.unsupervised.attribute.PrincipalComponents -R 1.0 -A 5 -M -1\" -S 1 -num-slots 8 -I 100 "\
#            "-W weka.classifiers.meta.RandomCommittee -- -S 1 -num-slots 4 -I 10 "

descList        = ["elementsv2-SIFt"]#, "elementsv2-SIFt-xscore"]
CASF_SETS       = ["CASFv2007", "CASFv2013-refined"]#, "CASF14"]
TRAIN_SETS      = ["sampling_clusters10", "sampling_100"]

#################################################################
def convertCSV2ARFF(CSVfile, ARFFpath):
    '''
    convert CSVfile to ARFF format at ARFFPath using weka-3.6.11
    '''
    processes = set()
    batchFile = "/home/dat/WORK/dev/weka-3-6-11/convertCSV2ARFF.sh"
    SHFILE  = open(batchFile, 'w')
    #SHFILE.write("export CLASSPATH=/home/dat/WORK/dev/weka-3-6-11/weka.jar\n")
    SHFILE.write("cd /home/dat/WORK/dev/weka-3-6-11/\n")
    if os.path.isfile(CSVfile):
        SHFILE.write("java -Xmx6144m -cp weka.jar weka.core.converters.CSVLoader {0} > {1}.arff\n".
                     format( CSVfile, os.path.join(ARFFpath, os.path.splitext(os.path.basename(CSVfile))[0])) )
        SHFILE.close()
        cmd = "sh {0}".format(batchFile)
        processes.add(subprocess.Popen(cmd, shell=True))

    # check if all the child processes were closed
    for p in processes:
        if p.poll() is None:
            p.wait()
#################################################################
def convertCSVDir2ARFF(CSVpath, ARFFpath):
    for CSVfile in glob.glob(os.path.join(CSVpath, "*.csv")):
        convertCSV2ARFF(CSVfile, ARFFpath)
#################################################################
def createTrainingModel(batchFile, CASFset, trainingPrefix, classifier = "RotationForest", tmpTrainFile = "train.arff"):
    SHFILE  = open(batchFile, 'a')
    SHFILE.write("export CLASSPATH=/home/dat/WORK/dev/weka-3-7-12/weka.jar\n")
    for desc in descList:
        # create the right name for training set
        trainingName = os.path.join(trainingPath, "{0}_RMSD_{1}-{2}.arff".format(CASFset, trainingPrefix, desc))
        if not os.path.exists(trainingName):
            print("Training file not found ",trainingName)
            quit()

        line = cmdRemove.format(trainingName, tmpTrainFile)
        print(line)
        SHFILE.write(line)

        if classifier != "RandomForest":
            for base in baseClassifier.keys():
                dumpModel = os.path.join(testPath, "model", "{0}_RMSD_{1}_{2}_{3}-{4}.model"
                                         .format(CASFset, trainingPrefix, shortName[classifier], base, desc))
                SHFILE.write("echo {0}\n".format(dumpModel))
                CMD_TRAIN = PREFIX_JAVA + metaClassifier[classifier] + prefixTrainModel.format(tmpTrainFile) + dumpModel + suffixTrainModel + \
                            metaClassifierSetting[classifier] + baseClassifier[base] + " > dummy_stats.txt \n"
                            #metaClassifierSetting[classifier] + RANDOM_COMMITTEE + baseClassifier[base] + " > dummy_stats.txt \n"
                print(CMD_TRAIN)
                SHFILE.write(CMD_TRAIN)
        else:
            dumpModel = os.path.join(testPath, "model", "{0}_RMSD_{1}_{2}-{3}.model"
                                     .format(CASFset, trainingPrefix, shortName[classifier], desc))
            SHFILE.write("echo {0}\n".format(dumpModel))
            CMD_TRAIN = PREFIX_JAVA + metaClassifier[classifier] + prefixTrainModel.format(tmpTrainFile) + dumpModel + suffixTrainModel + \
                        metaClassifierSetting[classifier] + " > dummy_stats.txt \n"
            #metaClassifierSetting[classifier] + RANDOM_COMMITTEE + baseClassifier[base] + " > dummy_stats.txt \n"
            print(CMD_TRAIN)
            SHFILE.write(CMD_TRAIN)


    SHFILE.close()
#################################################################
def classifyTestModel(batchFile, testSet, CASFset, trainingPrefix, classifier = "RotationForest", tmpTestFile = "test.arff"):
    SHFILE  = open(batchFile, 'a')
    SHFILE.write("export CLASSPATH=/home/dat/WORK/dev/weka-3-7-12/weka.jar\n")

    for desc in descList:
        # create the right name for test set
        testName = os.path.join(testPath, "{0}_{1}.arff".format(testSet, desc))
        if not os.path.exists(testName):
            print("Test file not found ",testName)
            quit()

        line = cmdRemove.format(testName, tmpTestFile)
        print(line)
        SHFILE.write(line)

        if classifier != "RandomForest":
            for base in baseClassifier.keys():
                dumpModel = os.path.join(testPath, "model", "{0}_RMSD_{1}_{2}_{3}-{4}.model"
                                         .format(CASFset, trainingPrefix, shortName[classifier], base, desc))
                if not os.path.exists(dumpModel):
                    print("Training model not found ",dumpModel)
                    quit()
                resultName = os.path.join(resultPath, "{0}_{1}_{2}_{3}_{4}-{5}.csv".
                                          format(CASFset, trainingPrefix, shortName[classifier], base, testSet, desc))
                CMD_TEST = PREFIX_JAVA + metaClassifier[classifier] + prefixTestModel + dumpModel + suffixTestModel.format(tmpTestFile) + " > " + resultName + "\n"
                print(CMD_TEST)
                SHFILE.write(CMD_TEST)
        else:
            dumpModel = os.path.join(testPath, "model", "{0}_RMSD_{1}_{2}-{3}.model"
                                     .format(CASFset, trainingPrefix, shortName[classifier], desc))
            if not os.path.exists(dumpModel):
                print("Training model not found ",dumpModel)
                quit()
            resultName = os.path.join(resultPath, "{0}_{1}_{2}_{3}-{4}.csv".
                                      format(CASFset, trainingPrefix, shortName[classifier], testSet, desc))
            CMD_TEST = PREFIX_JAVA + metaClassifier[classifier] + prefixTestModel + dumpModel + suffixTestModel.format(tmpTestFile) + " > " + resultName + "\n"
            print(CMD_TEST)
            SHFILE.write(CMD_TEST)

    SHFILE.close()
#################################################################
def CSAR():
    batchFile = "/home/dat/WORK/dev/weka-3-7-12/performScoring_DIG"
    DBSet = ["SP", "XP", "asp", "plp", "chemscore", "goldscore"]
    #createTrainingModel(batchFile+"_training.sh", trainingSet="_refined_")
    createTrainingModel(batchFile+"_training.sh", trainingSet="_training_")
    for eachset in DBSet:
        classifyTestModel(batchFile+"_test.sh", trainingSet="_refined_", DBsetPrefix="DIG10.2_", DBsetPostfix=eachset)

    #batchFile = "/home/dat/WORK/dev/weka/performScoring.sh"
#    batchFile = "/home/dat/WORK/dev/weka-3-7-12/performScoring.sh"
#    createClassifyScriptPDBbind(batchFile)

    #JelenaAllSets = ["140722_set1_maestro_", "140722_set2_maestro_", "140722_set3_maestro_"]
    #for eachset in JelenaAllSets:
     #   create<ClassifyScript(batchFile, eachset)
#################################################################
def DUDE():
    batchFile = "/home/dat/WORK/RMSD_DUDE/performScoring_DUDE"
    DBSet = ["RENI", "FGFR1", "ADA"]
    for eachset in DBSet:
        classifyTestModel(batchFile+"_test.sh", trainingSet="_refined_RMSD_", DBsetPrefix="DUD-E_", DBsetPostfix=eachset)
        #classifyTestModel(batchFile+"_test.sh", trainingSet="_reduced_RMSD_", DBsetPrefix="DUD-E_", DBsetPostfix=eachset)<
#################################################################
def RMSD():
    batchFile = "/home/dat/WORK/RMSD/performScoring_RMSD"
    #createTrainingModel(batchFile+"_training.sh", trainingSet="_refined_RMSD_")
    #createTrainingModel(batchFile+"_training.sh", trainingSet="_reduced_RMSD_")
    DBSet = ["SP", "XP", "asp", "plp", "chemscore", "goldscore"]
    for eachset in DBSet:
        #classifyTestModel(batchFile+"_test.sh", trainingSet="_reduced_RMSD_", DBsetPrefix="DIG10.2_", DBsetPostfix=eachset)
        classifyTestModel(batchFile+"_test.sh", trainingSet="_refined_RMSD_", DBsetPrefix="DIG10.2_", DBsetPostfix=eachset)
#################################################################
def createTrainAll():
    #batchFile = "/home/dat/WORK/dev/weka-3-7-12/train_{0}.sh".format(CASF_SETS[0])
    #createTrainingModel(batchFile, CASFset=CASF_SETS[0], trainingPrefix=TRAIN_SETS[0], tmpTrainFile="train.arff")

    for CASFset in CASF_SETS:
        for trainSet in TRAIN_SETS:
            batchFile = "/home/dat/WORK/dev/weka-3-7-12/train_{0}.sh".format(CASFset)
            createTrainingModel(batchFile, CASFset, trainingPrefix=trainSet, tmpTrainFile="train_{0}.arff".format(CASFset))
            createTrainingModel(batchFile, CASFset, trainingPrefix=trainSet, classifier="RandomForest", tmpTrainFile="train_{0}.arff".format(CASFset))
#################################################################
def createTestAll():
    #batchFile = "/home/dat/WORK/dev/weka-3-7-12/test{0}".format(CASFset)
    #classifyTestModel(batchFile+"_KDMs.sh", testSet = "T36_JMJ_Xray_test_gold", CASFset=CASF_SETS[0], trainingPrefix=trainingList[0])

    for CASFset in CASF_SETS:
        for trainSet in TRAIN_SETS:
            batchFile = "/home/dat/WORK/dev/weka-3-7-12/test{0}.sh".format(CASFset)
            ############### Sirt2 from Berin ###############
            testSet = "Aminothiazoles_71_PB_md1_rst_Dat"
            classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, tmpTestFile="test_{0}.arff".format(CASFset))
            classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, classifier="RandomForest", tmpTestFile="test_{0}.arff".format(CASFset))
            ############### SmHDAC8 from Jelena ###############
            testSet = "SmHDAC8_inhibitors"
            classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, tmpTestFile="test_{0}.arff".format(CASFset))
            classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, classifier="RandomForest", tmpTestFile="test_{0}.arff".format(CASFset))
            ############### KDMs from Prof. Sippl ###############
            for evalSet in ["test_gold", "actives", "inactives"]:
                testSet = "T36_JMJ_Xray_{0}".format(evalSet)
                classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, tmpTestFile="test_{0}.arff".format(CASFset))
                classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, classifier="RandomForest", tmpTestFile="test_{0}.arff".format(CASFset))
            ############### DIG from CSAR2013 ###############
            for evalSet in ["XP", "SP", "goldscore"]:
                testSet = "DIG_{0}".format(evalSet)
                classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, tmpTestFile="test_{0}.arff".format(CASFset))
                classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, classifier="RandomForest", tmpTestFile="test_{0}.arff".format(CASFset))
#################################################################
def createTestFidele():

    TARGET_LIST_FIDELE  = ["5P21", "4BBG", "3KKP", "1GS4", "2X9E", "3E37"]
    TARGET_DB_FIDELE    = ["africa", "npact"]
    POSES_GEN_LIST_FIDELE  = ["GS", "XP"]
    for CASFset in CASF_SETS:
        for trainSet in TRAIN_SETS:
            batchFile = "/home/dat/WORK/dev/weka-3-7-12/testFidele{0}.sh".format(CASFset)
            ############### anti-cancer targets from Fidele ###############
            for target in TARGET_LIST_FIDELE:
                for target_db in TARGET_DB_FIDELE:
                    for pose in POSES_GEN_LIST_FIDELE:
                        testSet = "{0}-{1}-{2}".format(target, target_db, pose)
                        classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, tmpTestFile="test_{0}.arff".format(CASFset))
                        classifyTestModel(batchFile, testSet, CASFset=CASFset, trainingPrefix=trainSet, classifier="RandomForest", tmpTestFile="test_{0}.arff".format(CASFset))
############# MAIN PART ########################
if __name__=='__main__':
    '''
    '''
    #convertCSV2ARFF("/home/dat/WORK/DB/DESCRIPTORS/RMSD/processed/CASFv2007_RMSD_sampling_clusters10-elementsv2-SIFt.csv", "/home/dat/WORK/arff/")
    convertCSVDir2ARFF("/home/dat/WORK/DB/DESCRIPTORS/Processed/", "/home/dat/WORK/arff/")
    #createTrainAll()
    createTestFidele()
    createTestAll()
