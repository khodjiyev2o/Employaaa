import pytest
from httpx import AsyncClient
from main import app




@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://localhost:8080"
                ) as client:
        yield client
        


