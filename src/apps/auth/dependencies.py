from typing import Annotated

from fastapi import Depends, Form, UploadFile, File

from .services import UserService
from .schemas import CreateUserSchema
from src.dependencies import SessionDep
from src.utils.media_handler import save_photo


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


ServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_create_user_form(
    username: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    profile_photo: UploadFile | None = File(None),
) -> CreateUserSchema:
    filename = await save_photo(profile_photo)

    return CreateUserSchema(
        username=username,
        phone_number=phone_number,
        password=password,
        password_confirm=password_confirm,
        profile_photo=filename,
    )


UserRegisterFormDep = Annotated[CreateUserSchema, Depends(get_create_user_form)]
