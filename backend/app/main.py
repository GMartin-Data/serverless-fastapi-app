from fastapi import FastAPI, HTTPException
from mangum import Mangum
from starlette import status

from .schemas import Item, ItemCreate

# In-memory "database"
fake_items_db = []
item_id_counter = 0

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK, tags=["🏠 Home"])
async def read_root():
    return {"message": "Hello World"}


@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=["🧺 Items"],
)
async def create_item(item_payload: ItemCreate):
    global item_id_counter
    item_id_counter += 1

    new_item_data = item_payload.model_dump()
    new_item_data["id"] = item_id_counter

    created_item_model = Item(**new_item_data)
    fake_items_db.append(created_item_model)
    return created_item_model


@app.get("/items/{item_id}", response_model=Item, tags=["🧺 Items"])
async def read_item(item_id: int):
    for item_in_db in fake_items_db:
        if item_in_db.id == item_id:
            return item_in_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.get("/items", response_model=list[Item], tags=["🧺 Items"])
async def read_all_items():
    return fake_items_db


@app.put("/items/{item_id}", response_model=Item, tags=["🧺 Items"])
async def update_item(item_id: int, item_update_payload: ItemCreate):
    for index, item_in_db in enumerate(fake_items_db):
        if hasattr(item_in_db, "id") and item_in_db.id == item_id:
            updated_item_data = item_update_payload.model_dump()

            updated_item = Item(id=item_in_db.id, **updated_item_data)

            fake_items_db[index] = updated_item
            return updated_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.delete(
    "/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["🧺 Items"]
)
async def delete_item(item_id: int):
    for idx, item_in_db in enumerate(fake_items_db):
        if hasattr(item_in_db, "id") and item_in_db.id == item_id:
            fake_items_db.pop(idx)
            return None  # Corresponds to 204 No Content

    # Exiting the loop means the item wasn't found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


# Create the handler function that AWS Lambda will invoke
handler = Mangum(app)
