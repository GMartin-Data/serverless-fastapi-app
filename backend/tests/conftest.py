from typing import AsyncIterator

from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from backend.app.main import app as fastapi_app


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    """
    Yield an `AsyncClient` instance, configured to make requests directly to
    the in-memory FastAPI 'fast
    """
    async with ASGITransport(app=fastapi_app) as transport:
        async with AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            yield client
