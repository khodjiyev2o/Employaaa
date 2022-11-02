import pytest
from httpx import AsyncClient
from main import app


from database.models import User

from .conftest_db import override_get_db
from users import hashing



@pytest.fixture(scope="session")
async def client(): 
    async with AsyncClient(
        app=app,
        base_url="http://localhost:8080",
        headers={'Content-Type': 'application/json'
          }) as client:
        yield client
        
        


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'



        
@pytest.fixture(autouse=True)
def create_user(tmpdir):  
    database = next(override_get_db())
    password=hashing.Hash.bcrypt('john123')
    new_user = User(email='john@gmail.com', password=password)
    database.add(new_user)
    database.commit()
    yield 
    database.query(User).filter(User.email == 'john@gmail.com').delete()
    database.commit()

