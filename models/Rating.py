from sqlalchemy import  Column, Text, SmallInteger
from  database.database import Base
from utils.utils import get_class_attributes

class Rating(Base):
    __tablename__ = 'ratings'

    movie_id = Column(Text, primary_key =True)
    user_id = Column(Text, primary_key =True)
    rating = Column(SmallInteger)
    skipped_fields=['skipped_fields','metadata','adult','homepage','poster_path','status']

    def attribute_names(self):
        names = []
        for (name,value) in get_class_attributes(self, self.skipped_fields):
            names.append(name)
        return names

    def attribute_values(self):
        values = []
        for (name, value) in get_class_attributes(self, self.skipped_fields):
            values.append(value)
        return values