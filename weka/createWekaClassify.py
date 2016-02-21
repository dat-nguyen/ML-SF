#!/home/dat/libs/miniconda3/bin/python3.5
# export PYTHONPATH=/mnt/zeus/dat/WORK/dev/ML-SF:$PYTHONPATH

__author__ = 'dat'

'''
\TODO: optimize + write comments

'''

import os.path

trainingPath    = "/home/dat/WORK/arff/"
testPath        = "/home/dat/WORK/arff/"
resultPath      = "/home/dat/WORK/output/results/2015-08-26/"

descList        = ["elementsv2-SIFt", "elementsv2-SIFt-xscore"]
trainingList    = ["CASF07", "CASF12", "CASF13", "CASF14"]

PREFIX_JAVA     = "java -Xmx23000M "
CLASSIFI        = "-t train.arff -T test.arff -c 1 -no-cv -o -classifications "
OUTPUT_CSV      = "\"weka.classifiers.evaluation.output.prediction.CSV\""
FILTER_PCA      = "\"weka.filters.unsupervised.attribute.PrincipalComponents -R 1.0 -A 5 -M -1\""
RANDOM_COMMITTEE = "-W weka.classifiers.meta.RandomCommittee -- -S 1 -num-slots 6 -I 10 "

shortName = {"RotationForest"   : "RoF",
             "Bagging"          : "Bagging",
             "RandomSubSpace"   : "RandSS"}

cmdRemove    = PREFIX_JAVA + "weka.filters.unsupervised.attribute.Remove -R first -i {0} -o {1}\n"
#cmdRename    = "java -Xmx25000M weka.filters.unsupervised.attribute.RenameAttribute -find \"scores\" -replace \"pKd.pKi\" -i "

metaClassifier  = {"RotationForest" : "weka.classifiers.meta.RotationForest ",
                   "Bagging"        : "weka.classifiers.meta.Bagging ",
                   "RandomSubSpace" : "weka.classifiers.meta.RandomSubSpace "}

metaClassifierSetting = {"RotationForest"   : " -G 3 -H 3 -P 50 -F " + FILTER_PCA + " -S 1 -num-slots 6 -I 100 ",
                         "Bagging"          : " -P 100 -S 1 -num-slots 6 -I 100 ",
                         "RandomSubSpace"   : " -P 0.5 -S 1 -num-slots 6 -I 100 "}
baseClassifier  = {"RoT"  : "-W weka.classifiers.trees.RandomTree -- -K 0 -M 1.0 -V 0.001 -S 1 ",
                   "REPT" : "-W weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L -1 -P -I 0.0 "}

# COMMAND = PREFIX_JAVA + metaClassifier + CLASSIFI + OUTPUT_CSV + metaClassifierSetting + RANDOM_COMMITTEE + baseClassifier



def createClassifyScriptPDBbind(batchFile):
    SHFILE  = open(batchFile, 'w')

    for trainingPrefix in trainingList:
        for desc in descList:
            # create the right name for training set
            trainingName = os.path.join(trainingPath, trainingPrefix+"_training_"+desc+".arff")
            if not os.path.exists(trainingName):
                print(trainingName)
            #    quit()

            line = cmdRemove.format(trainingName, "train.arff")
            #print(line)
            SHFILE.write(line)

            # for reproducing purpose
            #testName = os.path.join(testPath, trainingPrefix+"_training_"+desc+".arff")
            #line = cmdRemove + testName + " -o test.arff\n"
            #SHFILE.write(line)

            # for testing purpose
            testName = os.path.join(testPath, trainingPrefix+"_test_"+desc+".arff")
            if not os.path.exists(testName):
                print(testName)
            #    quit()

            line = cmdRemove.format(testName, "test.arff")
            #print(line)
            SHFILE.write(line)

            for metaClass in metaClassifier.keys():
                for baseClass in baseClassifier.keys():
                    resultName = os.path.join(resultPath, "{0}_test_{1}-{2}_{3}.csv".format(trainingPrefix, shortName[metaClass], baseClass, desc) )
                    #print(resultName)
                    line = PREFIX_JAVA + metaClassifier[metaClass] + CLASSIFI + OUTPUT_CSV \
                           + metaClassifierSetting[metaClass] + RANDOM_COMMITTEE + baseClassifier[baseClass] + " > " + resultName + "\n"
                    #print(line)
                    SHFILE.write(line)



    SHFILE.close()

# \TODO: NOT WORKING
def createClassifyScript(batchFile, trainingSet, DBsetPrefix, DBsetPostfix):

    SHFILE  = open(batchFile, 'a')

    for trainingPrefix in trainingList:
        for desc in descList:
            # create the right name for training set
            trainingName = os.path.join(trainingPath, trainingPrefix+trainingSet+desc+".arff")
            if not os.path.exists(trainingName):
                print(trainingName)
                quit()

            line = cmdRemove + trainingName + " -o train.arff\n"
            print(line)
            SHFILE.write(line)

            # create the right name for test set
            #testName = os.path.join(testPath, DBsetPrefix+desc+".arff")
            # for testing purpose
            testName = os.path.join(testPath, DBsetPrefix+desc+'_'+DBsetPostfix+".arff")
            if not os.path.exists(testName):
                print(testName)
                quit()

            line = cmdRemove + testName + " -o test.arff\n"
            print(line)
            SHFILE.write(line)

            for i in range(len(postCmdRoF_Methods)):
                resultName = os.path.join(resultPath, trainingPrefix+trainingSet+DBsetPrefix+cmdClassifyName+"-"+
                                          postCmdRoF_MethodsName[i]+"_"+desc+'_'+DBsetPostfix+".csv")
                line = cmdClassify + postCmdRoF + postCmdRoF_Methods[i] + " > " + resultName + "\n"
                print(line)
                SHFILE.write(line)
    SHFILE.close()

def CSAR():
#    batchFile = "/home/dat/WORK/dev/weka-3-7-12/performScoring_CSAR.sh"
#    DBSet = ["SP", "XP", "asp", "plp", "chemscore", "goldscore"]
#    for eachset in DBSet:
#       createClassifyScript(batchFile, trainingSet="_refined_", DBsetPrefix="DIG10.2_", DBsetPostfix=eachset)

    #batchFile = "/Users/knight/MyClouds/Python/performScoring.sh"
    batchFile = "/home/dat/WORK/dev/weka-3-7-12/performScoring.sh"
    createClassifyScriptPDBbind(batchFile)

############# MAIN PART ########################
if __name__=='__main__':
    '''
    '''
    #CSAR()
    #for metaClass in metaClassifier.keys():
    #    for baseClass in baseClassifier.keys():
            #cmd =
    #        print(cmd)


