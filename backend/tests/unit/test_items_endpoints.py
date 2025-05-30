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
    response = await async_client.post("/items/", json=item_payload)

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
    create_response = await async_client.post("/items/", json=item_payload)
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


@pytest.mark.asyncio
async def test_read_all_items_when_no_items_exist(async_client: AsyncClient):
    response = await async_client.get("/items/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    assert response.headers["content-type"] == "application/json"


@pytest.mark.asyncio
async def test_read_all_items_when_items_exist(async_client: AsyncClient):
    # Create a couple of items first
    item1_payload = {"name": "Item One", "price": 10.00}
    item2_payload = {
        "name": "Item Two",
        "description": "Description for item two",
        "price": 20.50,
        "is_offer": True,
    }

    response1 = await async_client.post("/items/", json=item1_payload)
    assert response1.status_code == status.HTTP_201_CREATED
    item1_data = response1.json()

    response2 = await async_client.post("/items/", json=item2_payload)
    assert response2.status_code == status.HTTP_201_CREATED
    item2_data = response2.json()

    # Then, get all items
    response_get_all = await async_client.get("/items/")
    assert response_get_all.status_code == status.HTTP_200_OK

    all_items = response_get_all.json()
    assert isinstance(all_items, list)
    assert len(all_items) == 2

    # ensure the structure and some key fileds of the returned data
    for item in all_items:
        assert "id" in item
        assert "name" in item
        assert "price" in item
        # Match again the created items
        if item["id"] == item1_data["id"]:
            assert item["name"] == item1_payload["name"]
        if item["id"] == item2_data["id"]:
            assert item["name"] == item2_payload["name"]

    assert response_get_all.headers["content-type"] == "application/json"


@pytest.mark.asyncio
async def test_update_item_success(async_client: AsyncClient):
    # First, create an item to update
    initial_payload = {
        "name": "Original Item",
        "description": "Original description.",
        "price": 10.00,
        "is_offer": False,
    }
    create_response = await async_client.post("/items/", json=initial_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created_item_id = create_response.json()["id"]

    # Data for updating the item
    update_payload = {
        "name": "Updated Item Name",
        "description": "Updated description.",
        "price": 12.50,
        "is_offer": True,
    }
    update_response = await async_client.put(
        f"/items/{created_item_id}", json=update_payload
    )

    assert update_response.status_code == status.HTTP_200_OK
    updated_item_data = update_response.json()
    assert updated_item_data["id"] == created_item_id  # ID should remain the same
    assert updated_item_data["name"] == update_payload["name"]
    assert updated_item_data["description"] == update_payload["description"]
    assert updated_item_data["price"] == update_payload["price"]
    assert updated_item_data["is_offer"] == update_payload["is_offer"]
    assert update_response.headers["content-type"] == "application/json"

    # Verify by GETting the item again
    get_response = await async_client.get(f"/items/{created_item_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["name"] == update_payload["name"]
    # Could have more tests but testing "name" seems already enough


@pytest.mark.asyncio
async def test_update_item_not_found(async_client: AsyncClient):
    non_existent_item_id = 99999  # Assuming this ID won't exist
    update_payload = {
        "name": "Non Existent Update",
        "description": "Attempt to update non-existent item.",
        "price": 5.00,
        "is_offer": False,
    }
    response = await async_client.put(
        f"/items/{non_existent_item_id}", json=update_payload
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    error_detail = response.json()
    assert error_detail["detail"] == "Item not found"


@pytest.mark.asyncio
async def test_update_item_invalid_price(async_client: AsyncClient):
    # First, create an item to update
    initial_payload = {"name": "Item for Price Test", "price": 20.00}
    create_response = await async_client.post("/items/", json=initial_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created_item_id = create_response.json()["id"]

    # Data with invalid price for updating
    update_payload_invalid_price = {
        "name": "Updated Item Name",
        "description": "Updated description.",
        "price": -5.00,  # Invalid price (must be > 0 based on ItemCreate via ItemBase)
        "is_offer": True,
    }
    response = await async_client.put(
        f"/items/{created_item_id}", json=update_payload_invalid_price
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # Then, check the detail of the validation error
    error_data = response.json()
    assert (
        "price" in error_data["detail"][0]["loc"]
    )  # Check that the error is related to 'price'


@pytest.mark.asyncio
async def test_delete_item_success(async_client: AsyncClient):
    # First, create an item to delete
    item_payload = {"name": "Item to Delete", "price": 7.77}
    create_response = await async_client.post("/items/", json=item_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created_item_id = create_response.json()["id"]

    # Delete the item
    delete_response = await async_client.delete(f"/items/{created_item_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    # For 204 No Content, there should be no response body
    assert not delete_response.content

    # Verify the item is actually deleted by trying to GET it
    get_response = await async_client.get(f"/items/{created_item_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_item_not_found(async_client: AsyncClient):
    non_existent_item_id = 99999  # Assuming this ID won't exist
    delete_response = await async_client.delete(f"/items/{non_existent_item_id}")

    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    error_detail = delete_response.json()
    assert error_detail["detail"] == "Item not found"
