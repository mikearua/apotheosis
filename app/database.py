from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@'
f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#THESE ARE SOME DEFAULT VALUES


def get_db():                    #this is the dependency
    db = SessionLocal()
    try:
        yield db
    finally:                               #THIS FUNC GETS A SESSION TO THE DATABASE
        db.close()
        
        
SECOND_DATABASE = 'postgresql://{settings.database_username}:{settings.database_password}@'
f'{settings.database_hostname}:{settings.database_port}/{settings.second_database_name}'

second_engine = create_engine(SECOND_DATABASE)

SecondSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=second_engine)
def sec_db():
    db = SecondSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
Base = declarative_base()

#INCASE WE WANT TO USE RAW SQL

#try:
#    conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='marvel2127', cursor_factory=RealDictCursor)
#    cursor = conn.cursor()
#    print("database connected")
#except Exception as error:
#    print("connection failed")
#    print("error", error)
#    time.sleep(2)
    #