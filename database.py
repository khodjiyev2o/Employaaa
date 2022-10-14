import databases
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("DATABASE_URL"))
print(os.environ.get("DATABASE_URL","not found"))
metadata = sqlalchemy.MetaData()
DATABASE_URL=f'postgresql://postgres:postgres@postgres:5432/postgres'

#DATABASE_URL = os.environ.get("DATABASE_URL")
db = databases.Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL
)



