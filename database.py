import databases,psycopg2,asyncpg
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os
load_dotenv()

metadata = sqlalchemy.MetaData()
DATABASE_URL=f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@postgres:5432/db'

db = databases.Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL
)



