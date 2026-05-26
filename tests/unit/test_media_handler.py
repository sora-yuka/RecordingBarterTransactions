import pytest
from fastapi import UploadFile, HTTPException, status
from unittest.mock import MagicMock, AsyncMock

from src.utils.media_handler import store_profile_photo, MAX_SIZE_IMAGE

pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_store_profile_photo_invalid_type():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "photo.jpg"
    mock_file.content_type = "application/pdf"

    with pytest.raises(HTTPException) as e:
        await store_profile_photo(mock_file)

    assert e.value.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_store_profile_photo_too_large():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "photo.jpg"
    mock_file.content_type = "image/jpeg"
    mock_file.read = AsyncMock(return_value=b"x" * (MAX_SIZE_IMAGE + 1))

    with pytest.raises(HTTPException) as e:
        await store_profile_photo(mock_file)

    assert e.value.status_code == status.HTTP_400_BAD_REQUEST
