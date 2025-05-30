from fastapi import APIRouter, HTTPException
from starlette import status

from ..db import fake_items_db, get_next_item_id
from ..schemas import Item, ItemCreate

router = APIRouter()


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item_payload: ItemCreate):
    new_id = get_next_item_id()

    new_item_data = item_payload.model_dump()
    new_item_data["id"] = new_id

    created_item_model = Item(**new_item_data)
    fake_items_db.append(created_item_model)
    return created_item_model


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item_in_db in fake_items_db:
        if hasattr(item_in_db, "id") and item_in_db.id == item_id:
            return item_in_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.get("/", response_model=list[Item])
async def read_all_items():
    return fake_items_db


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update_payload: ItemCreate):
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
)
async def delete_item(item_id: int):
    for idx, item_in_db in enumerate(fake_items_db):
        if hasattr(item_in_db, "id") and item_in_db.id == item_id:
            fake_items_db.pop(idx)
            return None  # Corresponds to 204 No Content

    # Exiting the loop means the item wasn't found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
