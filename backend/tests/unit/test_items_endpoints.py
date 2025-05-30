import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_create_item_success(async_client: AsyncClient):
    item_payload = {
        "name": "Test Item",
        "description": "This is a test item.",
        "price": 9.99,
        "is_offer": True,
    }
    response = await async_client.post("/items", json=item_payload)

    assert response.status_code == status.HTTP_201_CREATED

    created_item = response.json()
    assert "id" in created_item
    assert isinstance(created_item["id"], int)
    assert created_item["name"] == item_payload["name"]
    assert created_item["description"] == item_payload["description"]
    assert created_item["price"] == item_payload["price"]
    assert created_item["is_offer"] == item_payload["is_offer"]
    assert response.headers["content-type"] == "application/json"
