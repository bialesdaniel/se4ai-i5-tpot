import pandas as pd
from tpot import TPOTClassifier

def main():


    pipeline_optimizer = TPOTClassifier()

def prep_data():
    movies = pd.read_csv('movie-data.csv')
    users = pd.read_csv('users-data.csv')
    ratings = pd.read_csv('ratings-data.csv')