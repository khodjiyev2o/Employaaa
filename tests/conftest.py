import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import pytest
from dotenv import load_dotenv

from database.models import Base
from database.database import get_db,engine
from main import app
from httpx import AsyncClient
from contextlib import asynccontextmanager


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

@pytest.fixture(scope='module')
async def new_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)




# import asyncio
# import json
# from typing import Generator
# import pytest_asyncio
# from httpx import AsyncClient
# from sqlalchemy.orm import sessionmaker

# from sqlmodel.ext.asyncio.session import AsyncSession




# from database.database import engine
# from database.models import Base
# from main import app


# @pytest_asyncio.fixture
# async def async_client():
#    async with AsyncClient(
#             app=app,
#             base_url="http://localhost:8080"
#    ) as client:
#        yield client
       
       
      
# @pytest_asyncio.fixture(scope="function")
# async def async_session() -> AsyncSession:
#    session = sessionmaker(
#        engine, expire_on_commit=False
#    )

#    async with session as s:
#        async with engine.begin() as conn:
#            await conn.run_sync(Base.metadata.create_all)

#        yield s

#    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.drop_all)

#    await engine.dispose()





# @pytest.fixture(scope="session")
# def event_loop(request) -> Generator:  # noqa: indirect usage
#    loop = asyncio.get_event_loop_policy().new_event_loop()
#    yield loop
#    loop.close()
# SQLALCHEMY_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")







        
  