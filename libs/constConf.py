__author__ = 'dat'

#PROTEIN_DIR = '/home/dat/WORK/DB/'

PDBBIND_DIR = '/home/dat/WORK/DB/PDBbind/'

PROTEIN_INDEXFILE = ['/home/dat/WORK/DB/PDBbind/v2014-core/INDEX_core_data.2013',
                     '/home/dat/WORK/DB/PDBbind/v2013-core/INDEX_core_data.2013',
                     '/home/dat/WORK/DB/PDBbind/v2012-core/2012_core_data.lst',
                     '/home/dat/WORK/DB/PDBbind/v2007/INDEX.2007.core.data']

#lPROTEIN_DB_VER = ['v2014-refined', 'v2013-refined', 'v2012-refined', 'v2007']

OUTPUT_DIR = '/home/dat/WORK/output/'

GOLD_DOCKING_SCORE = ['asp', 'plp', 'chemscore', 'goldscore']
GLIDE_DOCKING_SCORE = ['SP', 'XP']


#lPROTEIN_STATUS = ['unprepared', 'prepared']

#lPROTEIN_DB = ['PDBbind', 'CSAR']

PROTEIN_SUFFIX = '_complex_prep_recep'
#PROTEIN_SUFFIX = '_protein_prep.pdb'
#PROTEIN_SUFFIX_MOL2 = '_protein_prep.mol2'

#LIGAND_SUFFIX_SDF = '_ligand.sdf'
#LIGAND_SUFFIX_MOL2 = '_ligand.mol2'
LIGAND_SUFFIX = '_complex_prep_lig'

EXT_MOL2    = '.mol2'
EXT_PDB     = '.pdb'
EXT_SDF     = '.sdf'
EXT_MAE     = '.maegz'

# for subprocess sending job
HOST_LIST   = ['athena', 'artemis', 'aphrodite', 'hades', 'poseidon', 'hydra', 'eos', 'hermes']
#HOST_LIST   = ['aphrodite', 'artemis', 'hades', 'athena', 'poseidon']
JOB_PER_HOST = 2
SSH_CMD     = "ssh -t -X "
