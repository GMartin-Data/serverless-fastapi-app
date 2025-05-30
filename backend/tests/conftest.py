from typing import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from backend.app.main import app as fastapi_app
from backend.app.main import fake_items_db, item_id_counter


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    """
    Yield an `AsyncClient` instance, configured to make requests directly to
    the in-memory FastAPI 'fastapi_app'.
    Resets the in-memory database before each test.
    """
    # Reseting the in-memory database and counter ensure test isolation for our
    # in-memory data
    global item_id_counter
    fake_items_db.clear()
    item_id_counter = 0

    async with ASGITransport(app=fastapi_app) as transport:
        async with AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            yield client
