from datetime import datetime
from typing_extensions import Self

from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class BaseUserSchema(BaseModel):
    username: str
    phone_number: PhoneNumber


class CreateUserSchema(BaseUserSchema):
    password: str = Field(min_length=6)
    password_confirm: str = Field(min_length=6, exclude=True)

    @model_validator(mode="after")
    def verify_password(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class ReadUserSchema(BaseUserSchema):
    id: int
    profile_photo: str | None
    created_at: datetime


class LoginSchema(BaseModel):
    phone_number: PhoneNumber
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
