__author__ = 'dat'

PDBBIND_DIR = '/home/dat/WORK/DB/PDBbind/'

PROTEIN_INDEXFILE = ['/home/dat/WORK/DB/PDBbind/v2014-core/INDEX_core_data.2013',
                     '/home/dat/WORK/DB/PDBbind/v2013-core/INDEX_core_data.2013',
                     '/home/dat/WORK/DB/PDBbind/v2012-core/2012_core_data.lst',
                     '/home/dat/WORK/DB/PDBbind/v2007/INDEX.2007.core.data']

CASF_VERSION = {'2007' : "v2007",
                '2012' : "v2012-refined",
                '2013' : "v2013-refined",
                '2014' : "v2014-refined"}

#lPROTEIN_DB_VER = ['v2014-refined', 'v2013-refined', 'v2012-refined', 'v2007']

OUTPUT_DIR = '/home/dat/WORK/output/'

GOLD_DOCKING_SCORE = ['asp', 'plp', 'chemscore', 'goldscore']
GLIDE_DOCKING_SCORE = ['SP', 'XP']

MAX_ANGSTROM = 10

#lPROTEIN_DB = ['PDBbind', 'CSAR']

PROTEIN_SUFFIX = '_complex_prep_recep'

LIGAND_SUFFIX = '_complex_prep_lig'

EXT_MOL2    = '.mol2'
EXT_PDB     = '.pdb'
EXT_SDF     = '.sdf'
EXT_MAE     = '.maegz'

# for subprocess sending job
HOST_LIST   = ['artemis', 'aphrodite', 'hades', 'hydra', 'eos', 'eros', 'hermes', 'hydra']
JOB_PER_HOST = 1
SSH_CMD     = "ssh -t -X "
