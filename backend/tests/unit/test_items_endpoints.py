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


@pytest.mark.asyncio
async def test_read_one_item_success(async_client: AsyncClient):
    # First, create an item to ensure it exists
    item_payload = {
        "name": "Readable Item",
        "description": "An item to be read.",
        "price": 15.50,
        "is_offer": False,
    }
    create_response = await async_client.post("/items", json=item_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created_item_id = create_response.json()["id"]

    # Now, try to read the created item
    read_response = await async_client.get(f"/items/{created_item_id}")

    assert read_response.status_code == status.HTTP_200_OK
    retrieved_item = read_response.json()
    assert retrieved_item["id"] == created_item_id
    assert retrieved_item["name"] == item_payload["name"]
    assert retrieved_item["description"] == item_payload["description"]
    assert retrieved_item["price"] == item_payload["price"]
    assert retrieved_item["is_offer"] == item_payload["is_offer"]
    assert read_response.headers["content-type"] == "application/json"


@pytest.mark.asyncio
async def test_read_one_item_not_found(async_client: AsyncClient):
    non_existent_item_id = 99999  # Assuming this ID won't exist
    response = await async_client.get(f"/items/{non_existent_item_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    # assert the structure of the default error message
    # FastAPI provides a default {"detail": "Not Found"}.
    error_detail = response.json()
    assert error_detail["detail"] == "Item not found"
