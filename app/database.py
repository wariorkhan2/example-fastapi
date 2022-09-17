from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#sqlalchemy_DATABASE_URL = 'postgresql://kali:kali@localhost/fastapi'


sqlalchemy_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(sqlalchemy_DATABASE_URL)

SessionLocal = sessionmaker(autocommit =False,autoflush = False, bind = engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='kali',password='kali', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connection to databse was successfull")
#         break
#     except Exception as error:
#         print("unable to connect")
#         print(error)
#         time.sleep(2)