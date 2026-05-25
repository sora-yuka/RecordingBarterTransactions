import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock

from src.apps.auth.routers import router
from src.apps.auth.dependencies import get_user_service


@pytest.fixture
def mock_auth_service() -> MagicMock:
    """Creates a mock UserService with async methods mocked out."""
    service = MagicMock()
    service.create_user = AsyncMock()
    service.authenticate_user = AsyncMock()
    service.generate_tokens = MagicMock()
    service.refresh_user_tokens = AsyncMock()
    service.get_current_user = AsyncMock()
    return service


@pytest.fixture
def client(mock_auth_service) -> TestClient:  # type: ignore
    """Create a test client with the UserService dependency overriden."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_user_service] = lambda: mock_auth_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
