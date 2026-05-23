from datetime import datetime
from typing_extensions import Self

from pydantic import BaseModel, Field, ConfigDict, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class BaseUserSchema(BaseModel):
    username: str
    phone_number: PhoneNumber


class CreateUserSchema(BaseUserSchema):
    profile_photo: str | None = None
    password: str = Field(min_length=6)
    password_confirm: str = Field(min_length=6, exclude=True)

    @model_validator(mode="after")
    def verify_password(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class ReadUserSchema(BaseUserSchema):
    id: int
    photo_url: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthorizeUserSchema(BaseModel):
    phone_number: PhoneNumber
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
