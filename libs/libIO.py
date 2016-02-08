'''
Created on 17.04.2013

@author: dat

input and output functions
'''

def createDisjointList(masterList, childList):
# create a new list that disjoints from master list and child list

    # conver childList to dict for faster find access
    childDict = {}
    for aList in childList:
        childDict[str(aList).lower()] = ''
    newList = []
    for aList in masterList:
        if aList not in childDict.keys():
            newList.append(str(aList).lower())
    return newList

def writeList2File(outList, outFile):
    OUTFILE = open(outFile, 'w')
    
    for aList in outList:
        OUTFILE.write(aList+'\n')
    
    OUTFILE.close()
    
def writeListWithScore2File(outList, scoreDict, outFile):
    OUTFILE = open(outFile, 'w')
    
    for aList in outList:
        OUTFILE.write(aList+'\t'+str(scoreDict[aList])+'\n')
    
    OUTFILE.close()    

# read dict file with each entry per line to a dict
def readDictFile(inFile):
    proteinDict = {}
    INFILE = open(inFile, 'r')
    
    for line in INFILE:
        tmpDict = line.split()
        proteinDict[str.lower(tmpDict[0])] = float(tmpDict[1])
    
    INFILE.close()
    return proteinDict

def readCSAR_KiFile(path):
    import os
    INFILE = open(os.path.join(path, "kd.dat"), 'r')
    for line in INFILE:
        #index   = int(line.split(' , ')[0])
        PDBname = str(line.split(' , ')[1])
        pKd     = float(line.split(' , ')[2])
        #print index, PDBname, pKd         
    INFILE.close()
#################################################################
# split mol2 filePath in multiple mol2 files
def splitMol2(filePath):
    FILE=open(filePath,'r')
    content=FILE.readlines()
    FILE.close()
    for i, v in enumerate(content):
        if v.find("@<TRIPOS>MOLECULE")!=(-1):
                index=i
                index=index+1
                fname=content[index]
                fname=fname.strip()
                fname=fname.rstrip('\n')
                fname=fname.replace(" ","_")
                fname=fname.replace("*","_")
                fname=fname.replace("#","_")
                fname=fname.replace("\\","_")
                fname=fname.replace("!","_")
                fname=fname.replace(";","_")
                fname=fname.replace(":","_")
                fname=fname.replace("?","_")
                fname="{0}_{1}.mol2".format(fname,i)
                #print(fname)
                r=open(fname,'w')
                r.writelines(v)
                i=i+1
                while (content[i].find("@<TRIPOS>MOLECULE")==(-1)):
                        r.writelines(content[i])
                        i=i+1
                        if i>=len(content):
                                break
                r.close()
                i=i-1
    return 0 # for no error
#################################################################
