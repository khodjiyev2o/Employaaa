import pytest
from httpx import AsyncClient
from authentication.auth import AuthHandler
from main import app

authhandler = AuthHandler()

base_url = "http://localhost:8080"

@pytest.mark.anyio
async def test_read_main(client:AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "working"}
    
# @pytest.mark.anyio
# async def test_all_users(client:AsyncClient):
#         user_access_token = authhandler.encode_token("john@gmail.com")
#         response = await client.get("/users/all/", headers={'Authorization': f'Bearer {user_access_token}'})
#         assert response.status_code == 200
        
        
        
@pytest.mark.anyio
async def test_all_users():
    async with AsyncClient(app=app, base_url=base_url) as client:
        user_access_token = authhandler.encode_token("john@gmail.com")
        response = await client.get("/users/all/", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200