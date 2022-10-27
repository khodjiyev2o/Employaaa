import databases
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
import asyncio
from redis_om import get_redis_connection



load_dotenv()

metadata = sqlalchemy.MetaData()


DATABASE_URL = os.environ.get("DATABASE_URL")

database = databases.Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL
)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



redis_db =  get_redis_connection(
    host= 'localhost', port='6379'
)