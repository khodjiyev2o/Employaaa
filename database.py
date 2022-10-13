import databases
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os
load_dotenv()

metadata = sqlalchemy.MetaData()
DATABASE_URL=f'postgresql://postgres:postgres@postgres:5432/postgres'

db = databases.Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL
)



