__author__ = 'dat'

'''
    create ML training model in weka

'''

import os.path


#trainingPath    = "/home/dat/arff/DIG10.2/"
#testPath        = "/home/dat/arff/DIG10.2/"
trainingPath    = "/home/dat/WORK/arff/"
testPath        = "/home/dat/WORK/arff/"

resultPath      = "/home/dat/WORK/output/results/2016-02-23/"

# for Jelena's data
#testPath        = "/home/dat/arff/Jelena/"
#resultPath      = "/home/dat/WORK/dev/weka/results/"
#prefixRemove    = "java -Xmx25000M weka.filters.unsupervised.attribute.Remove -R last -i "
#prefixRename    = "java -Xmx25000M weka.filters.unsupervised.attribute.RenameAttribute -find \"ID\" -replace \"pKd.pKi\" -i "
cmdRemove    = "java -Xmx30000M weka.filters.unsupervised.attribute.Remove -R first -i "
cmdRename    = "java -Xmx30000M weka.filters.unsupervised.attribute.RenameAttribute -find \"scores\" -replace \"pKd.pKi\" -i "

cmdDumpModel1  = "java -Xmx30000M weka.classifiers.meta.RotationForest -t train.arff -d "
cmdDumpModel2  = " -c 1 -no-cv -G 3 -H 3 -P 50 -F "

cmdTestModel1 = "java -Xmx30000M weka.classifiers.meta.RotationForest -l "
cmdTestModel2 = " -T test.arff -c 1 -v -o -classifications \"weka.classifiers.evaluation.output.prediction.CSV\" "

cmdClassify  = "java -Xmx30000M weka.classifiers.meta.RotationForest -t train.arff -T test.arff -c 1 -no-cv -o -classifications " \
                        "\"weka.classifiers.evaluation.output.prediction.CSV\" -G 3 -H 3 -P 50 -F "
#                "java -Xmx25000M weka.classifiers.trees.RandomForest -t train.arff -T test.arff -c 1 -no-cv -o -classifications " \
#                        "\"weka.classifiers.evaluation.output.prediction.CSV\" -I 500 -K 0 -S 1 -num-slots 4 "]

cmdClassifyName = "RoF"

postCmdRoF = "\"weka.filters.unsupervised.attribute.PrincipalComponents -R 1.0 -A 5 -M -1\" -S 1 -num-slots 4 -I 10 " #\
             #"-W weka.classifiers.meta.RandomCommittee -- -S 1 -num-slots 4 -I 10 "

postCmdRoF_Methods  = ["-W weka.classifiers.trees.RandomTree -- -K 0 -M 1.0 -V 0.001 -S 1",
                       "-W weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L -1 -P -I 0.0"]

postCmdRoF_MethodsName = ["RT", "REP"]

descList    = ["elementsv2-SIFt"]#, "elementsv2-SIFt-xscore"]
#binsizeList = [0]
#cutoff      = 12
#trainingList = ["CASF12", "CASF13"]#, "CASF14"]
trainingList = ["sampling_clusters10", "sampling_100"]


def createTrainingModel(batchFile, trainingSet):
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

            for i in range(len(postCmdRoF_Methods)):
                dumpModel = os.path.join(resultPath, "model", trainingPrefix+trainingSet+cmdClassifyName+"-"+
                                          postCmdRoF_MethodsName[i]+"_"+desc+".model")
                SHFILE.write("echo "+dumpModel+"\n")
                line = cmdDumpModel1 + dumpModel + cmdDumpModel2 + postCmdRoF + postCmdRoF_Methods[i] + " > dummy_stats.txt \n"
                print(line)
                SHFILE.write(line)

    SHFILE.close()

def classifyTestModel(batchFile, trainingSet, DBsetPrefix, DBsetPostfix):
    SHFILE  = open(batchFile, 'a')

    for trainingPrefix in trainingList:
        for desc in descList:
            # create the right name for test set
            #testName = os.path.join(testPath, DBsetPrefix+desc+".arff")
            # for testing purpose
            testName = os.path.join(testPath, DBsetPrefix+desc+'_'+DBsetPostfix+"_process.arff")
            if not os.path.exists(testName):
                print(testName)
                quit()

            line = cmdRemove + testName + " -o test.arff\n"
            print(line)
            SHFILE.write(line)

            for i in range(len(postCmdRoF_Methods)):
                dumpModel = os.path.join(resultPath, "model", trainingPrefix+trainingSet+cmdClassifyName+"-"+
                                          postCmdRoF_MethodsName[i]+"_"+desc+".model")
                if not os.path.exists(dumpModel):
                    print(dumpModel)
                    quit()
                SHFILE.write("echo "+dumpModel+"\n")
                resultName = os.path.join(resultPath, trainingPrefix+trainingSet+DBsetPrefix+cmdClassifyName+"-"+
                                          postCmdRoF_MethodsName[i]+"_"+desc+'_'+DBsetPostfix+".csv")
                line = cmdTestModel1 + dumpModel + cmdTestModel2 + " > " + resultName + "\n"
                print(line)
                SHFILE.write(line)

    SHFILE.close()

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

def DUDE():
    batchFile = "/home/dat/WORK/RMSD_DUDE/performScoring_DUDE"
    DBSet = ["RENI", "FGFR1", "ADA"]
    for eachset in DBSet:
        classifyTestModel(batchFile+"_test.sh", trainingSet="_refined_RMSD_", DBsetPrefix="DUD-E_", DBsetPostfix=eachset)
        #classifyTestModel(batchFile+"_test.sh", trainingSet="_reduced_RMSD_", DBsetPrefix="DUD-E_", DBsetPostfix=eachset)

def RMSD():
    batchFile = "/home/dat/WORK/RMSD/performScoring_RMSD"
    #createTrainingModel(batchFile+"_training.sh", trainingSet="_refined_RMSD_")
    #createTrainingModel(batchFile+"_training.sh", trainingSet="_reduced_RMSD_")
    DBSet = ["SP", "XP", "asp", "plp", "chemscore", "goldscore"]
    for eachset in DBSet:
        #classifyTestModel(batchFile+"_test.sh", trainingSet="_reduced_RMSD_", DBsetPrefix="DIG10.2_", DBsetPostfix=eachset)
        classifyTestModel(batchFile+"_test.sh", trainingSet="_refined_RMSD_", DBsetPrefix="DIG10.2_", DBsetPostfix=eachset)


############# MAIN PART ########################
if __name__=='__main__':
    '''
    '''
    #RMSD()
    #CSAR()
    #DUDE()

