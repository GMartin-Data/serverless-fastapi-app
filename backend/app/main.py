from fastapi import FastAPI
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
    tags=["🆕 Items"],
)
async def create_item(item_payload: ItemCreate):
    global item_id_counter
    item_id_counter += 1

    new_item_data = item_payload.model_dump()
    new_item_data["id"] = item_id_counter

    created_item_model = Item(**new_item_data)
    return created_item_model


# Create the handler function that AWS Lambda will invoke
handler = Mangum(app)
