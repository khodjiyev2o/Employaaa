import pytest
from httpx import AsyncClient



@pytest.mark.anyio
async def test_read_main(client:AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "working"}
    
# from main import app    
# import pytest
# from httpx import AsyncClient




# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(app=app, base_url="http://localhost:8080") as ac:
#         response = await ac.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"status": "working"}
 