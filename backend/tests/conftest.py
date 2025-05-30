from typing import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from backend.app.db import reset_db_state
from backend.app.main import app as fastapi_app


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    """
    Yield an `AsyncClient` instance, configured to make requests directly to
    the in-memory FastAPI 'fastapi_app'.
    Resets the in-memory database before each test.
    """
    # Reseting the in-memory database and counter ensure test isolation for our
    # in-memory data
    reset_db_state()

    async with ASGITransport(app=fastapi_app) as transport:
        async with AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            yield client
