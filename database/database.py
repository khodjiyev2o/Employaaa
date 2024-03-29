import databases
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
import aioredis
from contextlib import asynccontextmanager


load_dotenv()

metadata = sqlalchemy.MetaData()


DATABASE_URL = os.environ.get('DATABASE_URL')

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



redis_db = aioredis.from_url(os.environ.get("REDIS_URL"),decode_responses=True)

