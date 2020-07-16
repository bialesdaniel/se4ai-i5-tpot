from os import getenv, getcwd

GENERATIONS = int(getenv('GENERATIONS', 100))
POPULATION_SIZE = int(getenv('POPULATION_SIZE', 100))
RANDOM_STATE = int(getenv('RANDOM_STATE', 42))
TARGET_CACHE_SIZE = int(getenv('TARGET_CACHE_SIZE', 1))
CACHE_CLEAR_FREQUENCY = int(getenv('CACHE_CLEAR_FREQUENCY', 30))
N_JOBS = int(getenv('N_JOBS', 1))
OUTPUT_DIRECTORY = getenv('OUTPUT_DIRECTORY', '{ROOT_DIR}/tpot-output'.format(ROOT_DIR=getcwd()))
DATASET_SIZE = int(getenv('TRAINING_SIZE', -1))
VERBOSITY = int(getenv('VERBOSITY', 0))

def get_verbosity(tool_name):
    tool_name = tool_name.lower()
    if tool_name  == 'tpot':
        return VERBOSITY
    if tool_name == 'joblib_memory':
        return 1 if VERBOSITY == 3 else 0
    if tool_name == 'pipeline':
        return VERBOSITY > 1
    if tool_name == 'cache':
        return VERBOSITY == 3
    raise ValueError('unrecognized tool_name')
    