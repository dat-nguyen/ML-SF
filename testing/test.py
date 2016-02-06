import os

from libs import libIO
from libs import libRMSD
from libs.constConf import *
from libs.ioPDBbind import *

#splitMol2(sys.argv[1])
print(os.getcwd())
#os.chdir("/home/dat/WORK/output/test/")
#rmsds = libRMSD.calcRMSDPoses("ligand.mol2", "/home/dat/WORK/output/RMSD/v2007/gold/goldscore/1gvw/")
#rmsds = libRMSD.calcRMSDPoses("ligand.mol2", "/home/dat/WORK/output/test/", prefix="_")
#libIO.splitMol2("test.mol2")
CASFyear = "2012"
proteinDir  = CASF_PATH[CASFyear]
indexFile   = CASF_REFINED_INDEX[CASFyear]
data1 = parse_index(proteinDir, indexFile)

CASFyear = "2014"
proteinDir  = CASF_PATH[CASFyear]
indexFile   = CASF_REFINED_INDEX[CASFyear]
data2 = parse_index(proteinDir, indexFile)

#newProt = libIO.createDisjointList(data2.keys(), data1.keys())
#print(len(newProt), newProt)

#from libs import libGlide
#libGlide.convertPosesToMOL2("2007", "SP")