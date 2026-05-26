from src.apps.auth.repositories import UserRepository
from src.apps.auth.schemas import CreateUserSchema, ReadUserSchema, AuthorizeUserSchema, TokenSchema
from src.apps.auth.authentications import (
    create_access_token,
    create_refresh_token,
    decode_token,
    TokenType,
)
from src.apps.auth.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
)
from src.utils.password_handler import password_hasher


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: CreateUserSchema) -> ReadUserSchema:
        if await self.repository.get_by_field(phone_number=user_data.phone_number):
            raise UserAlreadyExistsException()

        data = user_data.model_dump()
        data["password"] = password_hasher.hash(data["password"])

        new_user = await self.repository.create(data)
        return ReadUserSchema.model_validate(new_user)

    async def get_current_user(self, credentials: str) -> ReadUserSchema:
        payload = decode_token(token=credentials)

        user = await self.repository.get_by_field(id=int(payload.get("sub")))
        return ReadUserSchema.model_validate(user)


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def _build_tokens(self, user: ReadUserSchema) -> TokenSchema:
        token_payload = {"sub": str(user.id), "phone": user.phone_number}
        return TokenSchema(
            access_token=create_access_token(token_payload),
            refresh_token=create_refresh_token(token_payload),
        )

    async def authenticate_user(self, login_data: AuthorizeUserSchema) -> TokenSchema:
        user = await self.repository.get_by_field(phone_number=login_data.phone_number)
        if not user or not password_hasher.verify(login_data.password, user.password):
            raise InvalidCredentialsException()
        return self._build_tokens(user)

    async def refresh_user_tokens(self, token: str) -> TokenSchema:
        payload = decode_token(token=token, expected_type=TokenType.REFRESH)
        user = await self.repository.get_by_field(id=int(payload.get("sub")))
        return self._build_tokens(user)
