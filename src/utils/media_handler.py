import uuid
import aiofiles
from pathlib import Path

from fastapi import UploadFile, HTTPException, status

UPLOAD_DIR = Path("uploads/profile-pics")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 5 * 1024 * 1025  # 5 MB


async def save_photo(profile_photo: UploadFile) -> str:
    filename = None

    if profile_photo and profile_photo.filename:
        if profile_photo.content_type not in ALLOWED_TYPES:
            print(profile_photo.content_type)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG, and WebP images are allowed",
            )

        contents = await profile_photo.read()
        if len(contents) > MAX_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image must be under 5 MB",
            )

        ext = Path(profile_photo.filename).suffix.lower()
        filename = f"{uuid.uuid4().hex}{ext}"
        async with aiofiles.open(UPLOAD_DIR / filename, "wb") as f:
            await f.write(contents)

        return filename
