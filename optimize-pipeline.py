from os import mkdir, getcwd
import pandas as pd
from joblib import dump, Memory
from threading import Thread
from pipelines.full_data_clean import create_data_clean_pipeline
from training.training import train_test_split, generate_optimal_pipeline, save_optimal_pipeline, cleanup_cache
from config.config import get_verbosity, OUTPUT_DIRECTORY, DATASET_SIZE

def movie_rating_train_optimal( memory ):

    try: mkdir(OUTPUT_DIRECTORY)
    except: pass

    # Load data
    movies_raw, users_raw, ratings_raw =  load_data()
    records = join_movies_users_ratings(movies_raw, users_raw, ratings_raw)
    records = records.sort_values(by=['user_id'])

    # Clean data
    records = records.dropna(subset=[
        'budget','popularity','revenue','runtime','vote_average','vote_count'
    ])
    data_clean_pipeline = create_data_clean_pipeline()
    features_all = data_clean_pipeline.fit_transform(records)
    outcomes_all = records['rating']
    
    # Save data clean pipeline
    dump(data_clean_pipeline, '{DIR}/data_clean_pipeline.joblib'.format(DIR=OUTPUT_DIRECTORY))

    # Find optimal pipeline
    features_train, outcomes_train, features_test, outcomes_test = train_test_split(
        features_all, outcomes_all, 80, limited_size=DATASET_SIZE
    )
    optimal_pipeline = generate_optimal_pipeline(features_train, outcomes_train, OUTPUT_DIRECTORY, memory)
    print('Optimal pipeline MSE: {MSE}'.format(
        MSE=str(optimal_pipeline.score(features_test, outcomes_test))
    ))

    #Save optimal pipeline
    save_optimal_pipeline(optimal_pipeline, OUTPUT_DIRECTORY)


def load_data():
    """ Load the data from the static data in the repo"""
    movies_raw = pd.read_csv('./movie-data.csv')
    users_raw = pd.read_csv('./users-data.csv')
    ratings_raw = pd.read_csv('./ratings-data.csv')
    return movies_raw, users_raw, ratings_raw

def join_movies_users_ratings(movies_raw, users_raw, ratings_raw):
    """ Combine our three data sets """
    users = users_raw.set_index('user_id')
    movies = movies_raw.set_index('movie_id')

    records = ratings_raw.join(users, on='user_id', how='left')
    records = records.join(movies, on='movie_id', how='left')
    return records


if __name__ == '__main__':
    # Start cache cleanup thread
    memory = Memory(location='{DIR}/cache'.format(DIR=OUTPUT_DIRECTORY), bytes_limit=10*2**30, verbose=get_verbosity('joblib_memory'))
    cleanup_thread = Thread(name='cache_cleanup', target=cleanup_cache(memory), daemon=True)
    cleanup_thread.start()

    # Start main program
    movie_rating_train_optimal( memory )