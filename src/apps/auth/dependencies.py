from typing import Annotated

from fastapi import Depends, Form, UploadFile, File

from src.dependencies import SessionDep, CredentialsDep
from src.apps.auth.repositories import UserRepository
from src.apps.auth.services import UserService, AuthService
from src.apps.auth.schemas import CreateUserSchema
from src.utils.media_handler import save_photo


def get_user_repository(session: SessionDep):
    return UserRepository(session)


RepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: RepositoryDep):
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_auth_service(repository: RepositoryDep):
    return AuthService(repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_create_user_form(
    username: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    profile_photo: UploadFile | None = File(None),
):
    filename = await save_photo(profile_photo)

    return CreateUserSchema(
        username=username,
        phone_number=phone_number,
        password=password,
        password_confirm=password_confirm,
        profile_photo=filename,
    )


UserFormDep = Annotated[CreateUserSchema, Depends(get_create_user_form)]
