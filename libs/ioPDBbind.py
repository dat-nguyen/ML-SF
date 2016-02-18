'''
Created on 17.04.2013

@author: dat

read and write function for PDBbind
'''

import os.path
import collections
import re


# some constants
PATHDB          = "/home/dat/WORK/DB/PDBbind/"

CLUSTERFILE     = 'v2012-refined/INDEX_core_cluster.2012'

PDBbindYear     = collections.namedtuple('Year', 'y2014 y2013 y2012 y2007')

CASF_NAME = {'2007' : "CASF07",
             '2012' : "CASF12",
             '2013' : "CASF13",
             '2014' : "CASF14"}

CASF_PATH = {'2007': PATHDB+"v2007",
             '2012': PATHDB+"v2012-refined",
             '2013': PATHDB+"v2013-refined",
             '2014': PATHDB+"v2014-refined"}

CASF_CORE_INDEX = {'2007' : "INDEX.2007.core.data_fix",
                   '2012' : "INDEX_core_cluster_fix.2012",
                   '2013' : "INDEX_core_data.2013",
                   '2014' : "INDEX_core_data.2013"}

CASF_CORE_INDEX_NAME = {'2007' : "INDEX.2007.core.name_fix",
                        '2012' : "INDEX_core_name.2012",
                        '2013' : "INDEX_core_name_fix.2013",
                        '2014' : "INDEX_core_name_fix.2013"}

CASF_REFINED_INDEX = {  '2007' : "INDEX.2007.refined.data",
                        '2012' : "INDEX_refined_data_fix.2012",
                        '2013' : "INDEX_refined_data_fix.2013",
                        '2014' : "INDEX_refined_data_fix.2014"}

dataFileCore    = PDBbindYear(y2014='v2014-core/INDEX_core_data.2013',
                              y2013='v2013-core/INDEX_core_data.2013',
                              y2012='v2012-refined/INDEX_core_data.2012',
                              y2007='v2007/INDEX.2007.core.data_fix')

nameFileCore    = PDBbindYear(y2014='v2014-core/INDEX_core_name.2013',
                              y2013='v2013-core/INDEX_core_name.2013',
                              y2012='v2012-refined/INDEX_core_name.2012',
                              y2007='v2007/INDEX.2007.core.name_fix')
dataFileRefined = PDBbindYear(y2014='v2014-refined/INDEX_refined_data_fix.2014',
                              y2013='v2013-refined/INDEX_refined_data_fix.2013',
                              y2012='v2012-refined/INDEX_refined_data_fix.2012',
                              y2007='v2007/INDEX.2007.refined.data')

nameFileRefined = PDBbindYear(y2014='v2014-refined/INDEX_refined_name.2014',
                              y2013='v2013-refined/INDEX_refined_name.2013',
                              y2012='v2012-refined/INDEX_refined_name.2012',
                              y2007='v2007/INDEX.2007.refined.name')

def readNameFile(nameFile):
# read ECnumber and protein name from name list file
# return a dict of tuples with key = protein id and 1.index = EC number, 2.index = protein name
    if not os.path.exists(nameFile):
        print("File not found ", nameFile)
        quit()
    
    FILE = open(nameFile, 'r')
    
    Protein = collections.namedtuple('Protein', 'ECnum name') 
    
    proteinDict = {}
    # read each line
    for line in FILE:
        # skip comments
        if not (line[0] == '#'):
            protein = line.split()
            if len(protein[1])==4: # detect release year entry, for PDBbind version after 2010
                tmpProtein = Protein(ECnum=protein[2], name=''.join(protein[3:]))
            else: # if no release year entry, then PDBbind version is prior 2010
                tmpProtein = Protein(ECnum=protein[1], name=''.join(protein[2:]))
            proteinDict[protein[0]] = tmpProtein
        
    FILE.close()
    return proteinDict

def readClusterFile(clusterFile):
# read cluster info (since PDBbind ver 2012)
    if not os.path.exists(clusterFile):
        print("File not found ", clusterFile)
        quit()   
    
    FILE = open(clusterFile, 'r')
    proteinDict = {}
    for line in FILE:
        # skip comment
        if not (line[0] == '#'):
            protein = line.split(None)            
            proteinDict[protein[0]] = ''.join(protein[5:6])
    
    FILE.close()
    return proteinDict
        

def readProteinInfo(dataFile, nameFile):
# read the whole protein information from PDBbind list file 
    if not os.path.exists(dataFile):
        print("File not found ", dataFile)
        quit()
    
    FILE = open(dataFile, 'r')

    Protein = collections.namedtuple('Protein', 'id resolution pKd Kd ECnum name cluster') 
    
    proteinList = []
    # read ECnumber and protein name
    proteinName = readNameFile(nameFile)
    
    # read each line
    for line in FILE:
        # skip comments
        if not (line[0] == '#'):
            protein = line.split(None)
            proteinID = protein[0]
            if protein[5] == '//': # detect refined protein list file, then cluster info is not available
                #print dataFile, (dataFile.find('refined'))
                if (dataFile.find('2012')>-1) and (dataFile.find('core')>-1): # 2012 data file doesnt contain cluster info anymore, get it from cluster file, ONLY FOR CORE DATA
                    tmpCluster = readClusterFile(PATHDB + CLUSTERFILE)[proteinID]
                else:
                    tmpCluster = ''  
            else: # cluster info is available (in core list file)
                tmpCluster = ''.join(protein[5:6])
            tmpProtein = Protein(id=proteinID, resolution=float(protein[1]), pKd=float(protein[3]), Kd=protein[4], ECnum=proteinName[proteinID].ECnum, name=proteinName[proteinID].name, cluster =tmpCluster)
            proteinList.append(tmpProtein)
        
    FILE.close()
    return proteinList

def convertList2Dict(proteinList):
# convert a protein list to dict with key = id and value = pKd
    proteinDict = {}
    for protein in proteinList:
        proteinDict[protein.id] = protein.pKd
    return proteinDict

def convertList2DictCluster(proteinList):
# convert a protein list to dict with key = id and value = cluster
    proteinDict = {}
    for protein in proteinList:
        proteinDict[protein.id] = protein.cluster
    return proteinDict

def createClusterDict_old(proteinList):
    """
    create a dict of cluster, with each entry is the protein IDs of this cluster
    """
    
    from operator import attrgetter
    
    cluster = ''
    clusterDict = {}
    proteinCluster = []
    for aProtein in sorted(proteinList, key=attrgetter('cluster', 'pKd', 'ECnum'), reverse = True):
        if aProtein.cluster != cluster: # detect new cluster
            clusterDict[cluster] = proteinCluster 
            proteinCluster = [aProtein.id]                        
            cluster = aProtein.cluster
        else: # same cluster
            proteinCluster.append(aProtein.id) # add the protein ID to the cluster
    # add the last cluster
    clusterDict[cluster] = proteinCluster
    # remove the empty key entry
    clusterDict.pop('', None)
    return clusterDict

def createClusterDict(data, clusterData):
    clusterDict = {}
    for proteinID in data.keys():
        cluster = clusterData[proteinID]["cluster"]
        #print(clusterDict.keys())
        if not cluster in clusterDict.keys(): # detect new cluster
            clusterDict[cluster] = [proteinID]
        else: # same cluster
            #print(data[proteinID]["pKx"])
            clusterDict[cluster].append(proteinID) # add the protein ID to the cluster
            #print(clusterDict[cluster])

    # remove the empty key entry
    clusterDict.pop('', None)
    #print(len(clusterDict.keys()))

    for cluster in clusterDict.keys():
        pKx = []
        for proteinID in clusterDict[cluster]:
            pKx.append(float(data[proteinID]["pKx"]))

        # sorting 2 lists together
        #sortedList = zip(*sorted(zip(pKx, clusterDict[cluster])))
        (pKx, sortedProteinID) = zip(*sorted(zip(pKx, clusterDict[cluster])))

        #sortedProteinID = list(sortedList)[1]
        #pKx = sortedList[0]

        clusterDict[cluster] = []
        for proteinID in sortedProteinID:
            clusterDict[cluster].append(proteinID)
    return (clusterDict)


def parse_index(path, index):
    '''
    parse PDBbind index file, path is the PDBbind directory
    '''
    regexp = r"""^
                (?P<pdb>\w{4})\s+
                (?P<resolution>\d[.]\d{2}|NMR)\s+
                (?P<year>\d{4})\s+
                (?P<pKx>\d{1,2}[.]\d{2})\s+
                (?P<type>\w{2,4})
                (?P<relation>[<>=~]{1,2})
                (?P<value>\d+[.]\d+|\d+)
                (?P<unit>\w{2})\s+
                (?P<cluster>[\s\d]+)"""
#(?P<unit>\w{2}).+\s+
    pattern = re.compile(regexp, re.VERBOSE)
    #print(index)
    data = {}
    for line in open(os.path.join(path,index)):
        if not line.startswith('#'):
            match = pattern.match(line)

            # PRINT A WARNING IF REGULAR EXPRESSION FAILED ON A LINE
            if not match:
                print("Could not parse line: {0}".format(line))
                continue

            rowdata = match.groupdict()
            pdb = rowdata.pop('pdb')
            data[pdb] = rowdata

    return data

    #return (PDBname, pKd)

# read the core index file and write pdb code to path
def readPDBcode(CASFyear, path):
    import os
    proteinDir  = CASF_PATH[CASFyear]
    indexFile   = CASF_CORE_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)

    outFile = os.path.join(path, '{0}_core_PDB.csv'.format(CASF_NAME[CASFyear]))
    CSVFILE = open(outFile, 'w')
    for proteinID in data.keys():
        CSVFILE.write(proteinID+'\n')
    CSVFILE.close()

#readPDBcode('2007', '/home/dat/WORK/DB/DESCRIPTORS/CASF/')

def parseClusterIndex(path, index):
    '''
    parse PDBbind index file, path is the PDBbind directory
    '''
    regexp = r"""^
                (?P<pdb>\w{4})\s+
                (?P<year>\d{4})\s+
                (?P<EC>(E.C.)[\d\-.]+)\s+
                (?P<cluster>.+)\s+"""

    pattern = re.compile(regexp, re.VERBOSE)

    data = {}
    for line in open(os.path.join(path,index)):
        if not line.startswith('#'):
            match = pattern.match(line)

            # PRINT A WARNING IF REGULAR EXPRESSION FAILED ON A LINE
            if not match:
                print("Could not parse cluster line: {0}".format(line))
                continue

            rowdata = match.groupdict()
            pdb = rowdata.pop('pdb')
            data[pdb] = rowdata

    return (data)

#cluster = parseClusterIndex("/home/dat/WORK/DB/PDBbind/v2013-refined/", "INDEX_core_name.2013")
#CLUSTER_FILE = open("/home/dat/WORK/DB/PDBbind/v2013-refined/INDEX_core_cluster.2013", 'w')

def createClusterDictFromYear(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    #proteinDir  = "/Users/knight/MyClouds/scores/"
    indexFile   = CASF_CORE_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    if (CASFyear == '2013' or CASFyear == '2014'):
        indexFile   = CASF_CORE_INDEX_NAME[CASFyear]
        clusterData = parseClusterIndex(proteinDir, indexFile)
        clusterDict = createClusterDict(data, clusterData)
    else:
        clusterDict = createClusterDict(data, data)

#    print(clusterDict)
    for cluster in clusterDict.keys():
        if len(clusterDict[cluster]) != 3:
            print(cluster, clusterDict[cluster])
    return (clusterDict)

def parseIndexFromYear(CASFyear):
    proteinDir  = CASF_PATH[CASFyear]
    #proteinDir  = "/Users/knight/MyClouds/scores/"
    indexFile   = CASF_CORE_INDEX[CASFyear]
    data = parse_index(proteinDir, indexFile)
    # getting cluster data from name file for core set > 2013
    if (CASFyear == '2013' or CASFyear == '2014'):
        indexFile   = CASF_CORE_INDEX_NAME[CASFyear]
        clusterData = parseClusterIndex(proteinDir, indexFile)
        for proteinID in data.keys():
            data[proteinID]["cluster"] = clusterData[proteinID]["cluster"]
    return (data)

#print(createClusterDictFromYear('2013'))
#print(parseIndexFromYear('2013'))