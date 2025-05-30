from fastapi import FastAPI
from mangum import Mangum
from starlette import status

from .routers import items

app = FastAPI(
    title="Serverless Item Management API",
    version="0.3.0",  # Corresponds to Phase 3 completion
    description="""
A simple API to manage items, demonstrating CRUD operations with FastAPI,
APIRouter for organization, Pydantic for data validation,
and preparation for serverless deployment. 🚀

**Key Features:**
- Create, Read, Update, and Delete (CRUD) operations for items.
- In-memory data storage for demonstration purposes.
- Auto-generated interactive API documentation.
    """,
)

# Include the items router
app.include_router(items.router, prefix="/items", tags=["🧺 Items"])


@app.get("/", status_code=status.HTTP_200_OK, tags=["🏠 Home"])
async def read_root():
    return {"message": "Hello World"}


# Create the handler function that AWS Lambda will invoke
handler = Mangum(app)
