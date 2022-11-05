import pytest
from httpx import AsyncClient

from authentication.auth import AuthHandler
from main import app
from .data import *
import json
authhandler = AuthHandler()


@pytest.mark.anyio
async def test_root(client:AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "working"}


@pytest.mark.anyio
async def test_token(client:AsyncClient):
    token = authhandler.encode_token(user.email)
    token_email = authhandler.decode_token(token)
    assert token_email == user.email
    
    


@pytest.mark.anyio
async def test_no_token(client:AsyncClient):
    response = await client.get("/users/1/")
    assert response.status_code == 403


# @pytest.mark.anyio
# async def test_new_user(client:AsyncClient):
#     response = await client.post("/users/create", json=dict(new_user))
#     assert response.status_code == 201
    

# @pytest.mark.anyio
# async def test_all_users(client:AsyncClient):
#     auth_token = authhandler.encode_token({"sub": f"{email}"})
#     headers = {"accept":"application/json",
#            "content-type":"application/json",
#            "Authorization": f"Bearer  {auth_token}"}
#     response = await client.get(f"/users/all",headers=headers)
#     assert response.status_code == 200  














