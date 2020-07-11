import csv
from database.database import create_base, load_session
create_base()
from models.Movie import Movie
from models.User import User
from models.Rating import Rating


def download_movie_data():
    session = load_session()
    movies = session.query(Movie).all()
    session.close()
    write_to_csv(movies,'movie-data')

def download_user_data():
    session = load_session()
    users = session.query(User).all()
    session.close()
    write_to_csv(users, 'users-data')

def download_rating_data():
    session = load_session()
    ratings = session.query(Rating).all()
    session.close()
    write_to_csv(ratings, 'ratings-data')
    

def write_to_csv(data_list, file_name):
    with open('{}.csv'.format(file_name), 'w',) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_list[0].attribute_names())
        for item in data_list:
            writer.writerow(item.attribute_values())


if __name__ == '__main__':
    download_movie_data()
    download_user_data()
    download_rating_data()