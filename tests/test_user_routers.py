import pytest
from httpx import AsyncClient

from authentication.auth import AuthHandler
from main import app
from schemas.users import UserSignIn
import json
authhandler = AuthHandler()


@pytest.mark.anyio
async def test_root(client:AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "working"}


@pytest.mark.anyio
async def test_token(client:AsyncClient):
    data=UserSignIn(
        email="string",
        password="string"
               )
    response = await client.post("/login",json=dict(data))
    token_email = authhandler.decode_token(response.json())
    assert token_email == data.email
    assert response.status_code == 200
    

    
    
@pytest.mark.anyio
async def test_no_token(client:AsyncClient):
    response = await client.get("/users/1/")
    assert response.status_code == 403


@pytest.mark.anyio
async def test_all_users(client:AsyncClient):
    email = "string"
    data=UserSignIn(
        email=email,
        password="string"
               )
    auth_token = authhandler.encode_token({"sub": f"{email}"})
    headers = {"accept":"application/json",
           "content-type":"application/json",
           "Authorization": f"Bearer  {auth_token}"}
    response = await client.get(f"/users/{email}/",headers=headers)
    assert response.status_code == 200  


# import pytest
# from httpx import AsyncClient
# from sqlalchemy import insert, select
# from sqlalchemy.ext.asyncio import AsyncSession

# from database.models import User


# @pytest.mark.asyncio
# async def test_create_user(
#        async_client: AsyncClient,
#        async_session: AsyncSession,
# ):
#    user_access_token = authhandler.encode_token({"sub": "john@gmail.com"})
#    response = await async_client.get("/users/all/", headers={'Authorization': f'Bearer {user_access_token}'})
#    assert response.status_code == 200











