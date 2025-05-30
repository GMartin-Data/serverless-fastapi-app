from fastapi import APIRouter, HTTPException, Path
from starlette import status

from ..db import fake_items_db, get_next_item_id
from ..schemas import Item, ItemCreate

router = APIRouter()


@router.post(
    "/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Item",
    description="""
Create a new item in the system.

You must provide:
- **name**: The name of the item (string, required).
- **price**: The price of the item (float, must be > 0, required).

Optionally, you can also provide:
- **description**: A textual description of the item (string).
- **is_offer**: A boolean flag indicating if the item is on offer (boolean).

The API will return the full item object, including its server-generated `id`.
    """,
)
async def create_item(item_payload: ItemCreate):
    """
    Handles the creation of a new item based on the provided payload.
    Generates a new ID, stores the item in memory, and returns the created item.
    """
    new_id = get_next_item_id()

    new_item_data = item_payload.model_dump()
    new_item_data["id"] = new_id

    created_item_model = Item(**new_item_data)
    fake_items_db.append(created_item_model)
    return created_item_model


@router.get(
    "/{item_id}",
    response_model=Item,
    summary="Get a Single Item by ID",
    description="Retrieve complete details for a specific item using its unique integer ID.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        }
    },
)
async def read_item(
    item_id: int = Path(
        ...,
        title="Item ID",
        description="The unique identifier of the item to retrieve.",
        examples=[1, 12, 33],
        ge=1,
    ),
):
    """
    Retrieves an item by its ID.
    Returns the item if found, otherwise raises a 404 error.
    """
    for item_in_db in fake_items_db:
        if hasattr(item_in_db, "id") and item_in_db.id == item_id:
            return item_in_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.get(
    "/",
    response_model=list[Item],
    summary="List All Items",
    description="Retrieve a list of all items currently stored in the system. The list will be empty if no items exist.",
)
async def read_all_items():
    """
    Retrieves all items from the in-memory database.
    Returns an empty list if no items are present.
    """
    return fake_items_db


@router.put(
    "/{item_id}",
    response_model=Item,
    summary="Update an Existing Item",
    description="""
Update an existing item by its ID.

You need to provide all fields for the item in the request body,
as this is a PUT operation (full replacement).
- **name**: The new name of the item.
- **price**: The new price (must be > 0).
- **description** (optional): The new description.
- **is_offer** (optional): The new offer status.
    """,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        },
        # status.HTTP_422_UNPROCESSABLE_ENTITY is automatically documented by FastAPI
        # when Pydantic validation fails for the request body (ItemCreate).
    },
)
async def update_item(
    item_id: int = Path(  # Use Path for more detailed path parameter documentation
        ...,
        title="Item ID",
        description="The ID of the item to update.",
        examples=[1, 12, 33],
        ge=1,  # Example validation: ID must be greater than or equal to 1
    ),
    *,
    item_update_payload: ItemCreate,
):
    """
    Updates an existing item with new data.
    The item to update is identified by its ID.
    All fields for the item must be provided in the request body.
    Returns the updated item if found, otherwise raises a 404 error.
    """
    for index, item_in_db in enumerate(fake_items_db):
        if hasattr(item_in_db, "id") and item_in_db.id == item_id:
            updated_item_data = item_update_payload.model_dump()

            updated_item = Item(id=item_in_db.id, **updated_item_data)

            fake_items_db[index] = updated_item
            return updated_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an Item by ID",
    description="Delete a specific item from the system using its unique integer ID. On successful deletion, no content is returned.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        }
        # No need to document 204 content here as it has no body.
        # The status_code=204 already informs clients.
    },
)
async def delete_item(
    item_id: int = Path(
        ...,
        title="Item ID",
        description="The unique identifier of the item to delete.",
        examples=[1, 12, 33],
        ge=1,
    ),
):
    """
    Deletes an item by its ID.
    Returns a 204 No Content response if successful, otherwise raises a 404 error.
    """
    for idx, item_in_db in enumerate(fake_items_db):
        if hasattr(item_in_db, "id") and item_in_db.id == item_id:
            fake_items_db.pop(idx)
            return None  # Corresponds to 204 No Content

    # Exiting the loop means the item wasn't found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
