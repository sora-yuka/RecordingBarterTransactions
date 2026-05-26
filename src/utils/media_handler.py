import uuid
import aiofiles
from pathlib import Path

from fastapi import UploadFile

from src.config.exceptions import BaseAppException, status

BASE_UPLOAD_DIR = Path("uploads")
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/mpeg", "video/quicktime", "video/webm"}
ALLOWED_TYPES = ALLOWED_IMAGE_TYPES | ALLOWED_VIDEO_TYPES
MAX_SIZE_IMAGE = 5 * 1024 * 1024  # 5 MB
MAX_SIZE_VIDEO = 50 * 1023 * 1024  # 50 MB


class InvalidMedia(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST


async def store_profile_photo(profile_photo: UploadFile, sub_dir: str) -> str:
    if profile_photo and profile_photo.filename:
        if profile_photo.content_type not in ALLOWED_IMAGE_TYPES:
            raise InvalidMedia("Only JPEG, PNG, and WebP images are allowed")

        contents = await profile_photo.read()
        if len(contents) > MAX_SIZE_IMAGE:
            raise InvalidMedia("Image must be under 5 MB")

        target_dir = BASE_UPLOAD_DIR / sub_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        ext = Path(profile_photo.filename).suffix.lower()
        filename = f"{uuid.uuid4().hex}{ext}"

        async with aiofiles.open(target_dir / filename, "wb") as f:
            await f.write(contents)

        return filename


async def upload_media_batch(files: list[UploadFile], sub_dir: str) -> list[str]:
    if not files:
        return []

    saved_filenames = []
    target_dir = BASE_UPLOAD_DIR / sub_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        if file and file.filename:
            if file.content_type not in ALLOWED_TYPES:
                raise InvalidMedia(f"File {file.filename} has an unsupported format.")

            is_video = file.content_type in ALLOWED_VIDEO_TYPES
            current_limit = MAX_SIZE_VIDEO if is_video else MAX_SIZE_IMAGE
            limit_text = "50 MB" if is_video else "5 MB"

            contents = await file.read()
            if len(contents) > current_limit:
                raise InvalidMedia(
                    f"File {file.filename} exceeds the {limit_text} limit."
                )

            ext = Path(file.filename).suffix.lower()
            filename = f"{uuid.uuid4().hex}{ext}"

            async with aiofiles.open(target_dir / filename, "wb") as f:
                await f.write(contents)

            saved_filenames.append(filename)

        return saved_filenames
