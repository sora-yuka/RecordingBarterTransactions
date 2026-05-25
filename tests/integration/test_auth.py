import pytest
from httpx import AsyncClient
from fastapi import status

pytestmark = pytest.mark.integration

VALID_USER = {
    "username": "testuser",
    "phone_number": "tel:+996-700-111-333",
    "password": "securepassword",
    "password_confirm": "securepassword",
}


@pytest.mark.asyncio
async def test_auth_enroll_success(client: AsyncClient):
    files = {"profile_photo": ("dummy.jpg", b"fake-bytes", "image/jpeg")}

    response = await client.post("/auth/enroll", data=VALID_USER, files=files)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["phone_number"] == VALID_USER["phone_number"]
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_auth_enroll_duplicate_user(client: AsyncClient):
    await client.post("/auth/enroll", data=VALID_USER)
    response = await client.post("/auth/enroll", data=VALID_USER)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["error"].lower()


@pytest.mark.asyncio
async def test_auth_enroll_missing_fields(client: AsyncClient):
    payload = VALID_USER.copy()
    payload.pop("password_confirm", None)
    response = await client.post("/auth/enroll", data=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_auth_enroll_empty_body(client: AsyncClient):
    response = await client.post("/auth/enroll")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_authorize_success(client: AsyncClient):
    await client.post("/auth/enroll", data=VALID_USER)
    response = await client.post("/auth/authorize", json=VALID_USER)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" and "refresh_token" in response.json()


@pytest.mark.asyncio
async def test_authorize_wrong_password(client: AsyncClient):
    await client.post("/auth/enroll", data=VALID_USER)
    response = await client.post(
        "/auth/authorize",
        json={"phone_number": VALID_USER["phone_number"], "password": "wrongpassword"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "incorrect" in response.json()["error"].lower()


@pytest.mark.asyncio
async def test_authorize_nonexistent_user(client: AsyncClient):
    response = await client.post("/auth/authorize", json=VALID_USER)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_authorize_missing_fields(client: AsyncClient):
    payload = VALID_USER.get("phone_number")
    response = await client.post("/auth/authorize", json={"phone_number": payload})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_refresh_success(client: AsyncClient):
    await client.post("/auth/enroll", data=VALID_USER)
    authorized = await client.post("/auth/authorize", json=VALID_USER)
    credentials = authorized.json().get("refresh_token")
    response = await client.post(
        "/auth/refresh", headers={"Authorization": f"Bearer {credentials}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" and "refresh_token" in response.json()
