from fastapi import FastAPI
from mangum import Mangum
from starlette import status


app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK, tags=["🏠 Home"])
async def read_root():
    return {"message": "Hello World"}


# Create the handler function that AWS Lambda will invoke
handler = Mangum(app)
