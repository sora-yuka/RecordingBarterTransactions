import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime, timezone
import io

from src.apps.auth.schemas import *
from src.apps.auth.exceptions import *

pytestmark = pytest.mark.unit


def test_register_success(client: TestClient, mock_auth_service: MagicMock) -> None:
    mock_file = "dummy.jpg"
    mock_user_data = ReadUserSchema(
        id=1,
        username="testuser",
        phone_number="tel:+996-700-111-333",
        photo_url=f"/uploads/profile-pics/{mock_file}",
        created_at=datetime.now(timezone.utc),
    )
    mock_auth_service.create_user.return_value = mock_user_data

    form_data = {
        "username": "testuser",
        "phone_number": "+996700111333",
        "password": "securepassword",
        "password_confirm": "securepassword",
    }
    files = {"profile_photo": (mock_file, io.BytesIO(b"file_content"), "image/jpeg")}
    response = client.post("/register", data=form_data, files=files)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_user_data.model_dump(mode="json")
    mock_auth_service.create_user.assert_called_once()


def test_register_already_exists(
    client: TestClient, mock_auth_service: MagicMock
) -> None:
    mock_auth_service.create_user.side_effect = UserAlreadyExistsException(
        "User already exists"
    )

    form_data = {
        "username": "existinguser",
        "phone_number": "tel:+996-700-111-333",
        "password": "securepassword",
        "password_confirm": "securepassword",
    }
    response = client.post("/register", data=form_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User already exists"


def test_login_success(client: TestClient, mock_auth_service: MagicMock) -> None:
    mock_user = MagicMock(id=1, phone_number="tel:+996-700-111-333")
    mock_token = TokenSchema(access_token="mock_access", refresh_token="mock_refresh")
    mock_auth_service.authenticate_user.return_value = mock_user
    mock_auth_service.generate_tokens.return_value = mock_token

    login_data = {"phone_number": "tel:+996-700-111-333", "password": "securepassword"}
    response = client.post("/login", json=login_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_token.model_dump(mode="json")
    mock_auth_service.authenticate_user.assert_called_once()
    mock_auth_service.generate_tokens.assert_called_once_with(1, "tel:+996-700-111-333")


def test_login_invalid_credentials(
    client: TestClient, mock_auth_service: MagicMock
) -> None:
    mock_auth_service.authenticate_user.side_effect = InvalidCredentialsException(
        "Invalid password"
    )

    login_data = {"phone_number": "tel:+996-700-111-333", "password": "wrongpassword"}
    response = client.post("/login", json=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid password"


def test_refresh_success(client: TestClient, mock_auth_service: MagicMock) -> None:
    mock_token = TokenSchema(
        access_token="new_access_token", refresh_token="new_refresh_token"
    )
    mock_auth_service.refresh_user_tokens.return_value = mock_token
    headers = {"Authorization": "Bearer mock_token"}
    response = client.post("/refresh", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_token.model_dump(mode="json")
    mock_auth_service.refresh_user_tokens.assert_called_once()


def test_refresh_invalid(client: TestClient, mock_auth_service: MagicMock) -> None:
    mock_auth_service.refresh_user_tokens.side_effect = TokenExpiredException(
        "Token has expired"
    )

    headers = {"Authorization": "Bearer expired_token"}
    response = client.post("/refresh", headers=headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token has expired"


def test_get_me_success(client: TestClient, mock_auth_service: MagicMock) -> None:
    mock_user_data = ReadUserSchema(
        id=1,
        username="testuser",
        phone_number="tel:+996-700-111-333",
        created_at=datetime.now(timezone.utc),
    )
    mock_auth_service.get_current_user.return_value = mock_user_data

    headers = {"Authorization": "Bearer valid_access_token"}
    response = client.get("/me", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_user_data.model_dump(mode="json")
    mock_auth_service.get_current_user.assert_called_once()
