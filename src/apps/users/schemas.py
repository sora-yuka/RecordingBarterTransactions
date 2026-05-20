from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class BaseUserSchema(BaseModel):
    username: str
    email: EmailStr
    phone_number: PhoneNumber


class UserCreateSchema(BaseUserSchema):
    password: str = Field(min_length=6)


class UserPublicSchema(BaseUserSchema):
    id: int
    photo_profile: str | None
    created_at: datetime
