from fastapi import FastAPI
from starlette import status


app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK, tags=["🏠 Home"])
async def read_root():
    return {"message": "Hello World"}
