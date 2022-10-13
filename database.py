import databases
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os
load_dotenv()

metadata = sqlalchemy.MetaData()
SQLALCHEMY_DATABASE_URL = "postgresql://os.getenv('POSTGRES_USER'):os.getenv('POSTGRES_PASSWORD')@postgresserver/db"
db = databases.DataBASE(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)



