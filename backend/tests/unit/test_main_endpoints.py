import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_read_root_returns_hello_world_and_200_status(async_client: AsyncClient):
    response = await async_client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}
