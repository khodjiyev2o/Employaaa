from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from database.database import  get_db
from main import app

from dotenv import load_dotenv
import os

SQLALCHEMY_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)



def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


