from sqlalchemy import Column, Integer, String
from Models.configDB import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    first_name = Column(String)
    language_code = Column(String)
