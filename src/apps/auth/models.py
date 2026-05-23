from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.config.database import Base


class UserModel(Base):
    __tablename__ = "users_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150))
    password: Mapped[str] = mapped_column(String(255))
    profile_photo: Mapped[str | None] = mapped_column(String(500), default=None)
    phone_number: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    @property
    def photo_url(self) -> str | None:
        if self.profile_photo:
            return f"/uploads/profile-pics/{self.profile_photo}"
        return None

    def __repr__(self) -> str:
        return f"User (id={self.id})"
