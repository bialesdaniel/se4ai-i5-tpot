import math
from os import mkdir
from datetime import date, datetime
import time
from tpot import TPOTRegressor
from joblib import dump
from config.config import get_verbosity, GENERATIONS, POPULATION_SIZE, RANDOM_STATE, N_JOBS, CACHE_CLEAR_FREQUENCY

def train_test_split(features, outcomes, percent_train, limited_size=-1):
    """
    Generate a training set and test set from data
    Parameters:
    - features: The feature set to train on. In scikit-learn this is often refered to as X.
    - outcomes: The labeled outcomes we are trying to predict. In scikit-learn this often refered to as y.
    - percent_train: The percent of the data to use for training. The rest will be used for test.
    - limited_size: If you don't want to train and test on all the data you can specify the amount of data you
                    want to use.
    Output:
    - features_train: The set of features for training
    - outcomes_train: The set of outcomes for training
    - features_test: The set of features for testing
    - outcomes_test: The set of outcomes for testing
    """
    if len(features) != len(outcomes):
        raise IndexError('the number of feautre instances and outcome instances do not match')
    if percent_train >= 100 or percent_train <= 0:
        raise ValueError('percent must be between 0 and 100')
    if limited_size > len(features):
        raise ValueError('limited size is larger than the number of instances provided')
    if limited_size <0:
        limited_size = len(features)

    features_set = features[:limited_size]
    outcomes_set = outcomes[:limited_size]
    train_size = math.ceil(len(features_set)*percent_train/100)
    features_train = features_set[:train_size - 1]
    outcomes_train = outcomes_set[:train_size - 1]
    features_test = features_set[train_size-1:]
    outcomes_test = outcomes_set[train_size-1:]
    return features_train, outcomes_train, features_test, outcomes_test

def generate_optimal_pipeline(features, outcomes, output_dir, memory=None):
    """
    Generate a training set and test set from data
    Parameters:
    - features: The feature set to train on. In scikit-learn this is often refered to as X.
    - outcomes: The labeled outcomes we are trying to predict. In scikit-learn this often refered to as y.
    - output_dir: The directory that TPOT can write to. This will be where the cache and intermitent save are written.
    Output:
    The TPOT object returned by fitting TPOTRegressor https://epistasislab.github.io/tpot/api/
    """
    if(features.shape[0] * features.shape[1] > (50000 * 250)):
        config_dict = 'TPOT light'
    else:
        config_dict = None

    pipeline_optimizer = TPOTRegressor(generations=GENERATIONS, population_size=POPULATION_SIZE, verbosity=get_verbosity('tpot'), 
                            random_state=RANDOM_STATE, template='Selector-Transformer-Regressor', n_jobs=N_JOBS,
                            warm_start=True, memory=memory, config_dict=config_dict, 
                            periodic_checkpoint_folder='{DIR}/tpot-intermediate-save/'.format(DIR=output_dir))
    
    pipeline_optimizer.fit(features, outcomes)
    return pipeline_optimizer

def cleanup_cache(memory):
    def infinite():
        verbose = get_verbosity('cache')
        while(True):
            if verbose: print('\nreducing size of tpot cache at {}'.format(datetime.now()))
            memory.reduce_size()
            if verbose: print('done cleaning; going to sleep for 30 min.')
            time.sleep(CACHE_CLEAR_FREQUENCY * 60)
    return infinite

def save_optimal_pipeline(optimal_pipeline, output_dir):
    try: mkdir('{DIR}/optimal'.format(DIR=output_dir))
    except: pass

    current_date = date.today()

    optimal_pipeline.export('{DIR}/optimal/{DATE}.py'.format(
        DIR=output_dir,
        DATE=current_date
    ))
    dump(optimal_pipeline.fitted_pipeline_, '{DIR}/fitted_pipeline_{DATE}.joblib'.format(
        DIR=output_dir,
        DATE=current_date
    ))