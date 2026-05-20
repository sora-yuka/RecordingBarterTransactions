from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.config.database import Base


class User(Base):
    __tablename__ = "users_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    profile_photo: Mapped[str | None] = mapped_column(String(200), default=None)
    phone_number: Mapped[str] = mapped_column(unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @property
    def photo_url(self) -> str | None:
        if self.profile_photo:
            return f"/media/profile-pics/{self.profile_photo}"
        return None

    def __repr__(self) -> str:
        return f"User (id={self.id})"
