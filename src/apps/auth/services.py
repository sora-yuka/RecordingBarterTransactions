from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel
from .schemas import CreateUserSchema, ReadUserSchema, AuthorizeUserSchema, TokenSchema
from .authentication import create_access_token, create_refresh_token, decode_token
from .exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
)
from src.utils.password_handler import password_hasher


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_user_by_field(self, **kwargs) -> UserModel | None:
        if not kwargs:
            return None
        filters = [getattr(UserModel, key) == val for key, val in kwargs.items()]
        result = await self.session.execute(select(UserModel).where(*filters))
        return result.scalars().one_or_none()

    async def create_user(self, user_data: CreateUserSchema) -> UserModel:
        if await self._get_user_by_field(phone_number=user_data.phone_number):
            raise UserAlreadyExistsException(
                "User with this phone number already exists"
            )

        data = user_data.model_dump()
        data["password"] = password_hasher.hash(data["password"])

        new_user = UserModel(**data)
        self.session.add(new_user)

        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def authenticate_user(self, login_data: AuthorizeUserSchema) -> UserModel:
        user = await self._get_user_by_field(phone_number=login_data.phone_number)

        if not user or not password_hasher.verify(login_data.password, user.password):
            raise InvalidCredentialsException("Incorrect phone number or password")

        return user

    def generate_tokens(self, user_id: int, phone_number: str) -> TokenSchema:
        token_payload = {"sub": str(user_id), "phone": phone_number}
        return TokenSchema(
            access_token=create_access_token(token_payload),
            refresh_token=create_refresh_token(token_payload),
        )

    async def refresh_user_tokens(self, refresh_token: str) -> TokenSchema:
        payload = decode_token(token=refresh_token, expected_type="refresh")

        user = await self._get_user_by_field(id=int(payload.get("sub")))

        return self.generate_tokens(user.id, user.phone_number)

    async def get_current_user(self, credentials_str: str) -> ReadUserSchema:
        payload = decode_token(token=credentials_str)

        user = await self._get_user_by_field(id=int(payload.get("sub")))
        return ReadUserSchema.model_validate(user)
