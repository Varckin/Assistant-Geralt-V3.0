from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URL = os.getenv('DB_URL')


engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=True)
Base = declarative_base()

def get_session():
    return Session(bind=engine)
