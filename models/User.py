from  database.database import Base
from utils.utils import get_class_attributes

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'autoload':True}

    skipped_fields=['skipped_fields','metadata']

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