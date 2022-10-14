import databases
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os
load_dotenv()

metadata = sqlalchemy.MetaData()
DATABASE_URL='postgresql://postgres:postgres@postgres:5432/postgres'

#did not work
#DATABASE_URL = os.environ.get("DATABASE_URL")
#DATABASE_URL = os.getenv("DATABASE_URL")


print(DATABASE_URL)
db = databases.Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL
)



