import os

from libs import libIO
from libs import libRMSD


#splitMol2(sys.argv[1])
print(os.getcwd())
os.chdir("/home/dat/WORK/output/test/")
#rmsds = libRMSD.calcRMSDPoses("ligand.mol2", "/home/dat/WORK/output/RMSD/v2007/gold/goldscore/1gvw/")
rmsds = libRMSD.calcRMSDPoses("ligand.mol2", "/home/dat/WORK/output/test/", prefix="_")
print(rmsds)
#libIO.splitMol2("test.mol2")