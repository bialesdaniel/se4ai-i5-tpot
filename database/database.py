import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = ''
engine = ''
def create_base():
    global Base, engine
    if Base == '' and engine =='':
        engine = db.create_engine('postgresql://{}:{}@{}:{}/{}'.format(
            os.getenv("RDS_USER"),
            os.getenv("RDS_PASSWORD"),
            os.getenv("RDS_HOST"),
            os.getenv("RDS_PORT"),
            os.getenv("RDS_DATABASE")
        ))
        Base = declarative_base(engine)
    return Base

def load_session():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session