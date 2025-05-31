from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# --- CORS Middleware Configuration ---
# Set the origins that are allowed to make requests
# For development, can be permissive
# For production, restrict this to the frontend's actual domain
origins = [
    "http://localhost",
    "http://localhost:8080",  # Common local dev server port
    "http://localhost:5500",  # Common VS Code Live Server port
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5500",
    "null",  # For 'file://' origin when opening index.html directly - BE CAREFUL WITH THIS
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Can also be ["*"] for development to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the items router
app.include_router(items.router, prefix="/items", tags=["🧺 Items"])


@app.get("/", status_code=status.HTTP_200_OK, tags=["🏠 Home"])
async def read_root():
    return {"message": "Hello World"}


# Create the handler function that AWS Lambda will invoke
handler = Mangum(app)
