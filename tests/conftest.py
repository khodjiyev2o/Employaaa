import pytest
from httpx import AsyncClient
from main import app


from database.models import users

from .conftest_db import override_get_db
from users import hashing



@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(
        app=app,
        base_url="http://localhost:8080",
        headers={'Content-Type': 'application/json'
          }) as client:
        yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture(autouse=True)
async def create_user(tmpdir):
    database = next(override_get_db())
    new_user = users.insert().values(email='john@gmail.com', password=hashing.Hash.bcrypt('john123'))
    await database.execute(new_user)
    yield    
    query = users.delete().where(users.c.email == 'john@gmail.com')
    await database.execute(query)

        


