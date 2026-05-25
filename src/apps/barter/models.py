from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.config.database import Base


class BarterMediaModel(Base):
    __tablename__ = "barter_media"

    id: Mapped[int] = mapped_column(primary_key=True)
    berter_id: Mapped[int] = mapped_column(ForeignKey("barters.id"))
    file_path: Mapped[str] = mapped_column(String(500))
    media_type: Mapped[str] = mapped_column(String(10))
    order: Mapped[int] = mapped_column(default=0)


class BarterModel(Base):
    __tablename__ = "barters"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users_account.id"))
    offered_title: Mapped[str] = mapped_column(String(150))
    offered_item_media: Mapped[list["BarterMediaModel"]] = relationship(
        "BarterMediaModel",
        backref="barter",
        cascade="all, delete-orphan",
        order_by="BarterMediaModel.order",
    )
    offered_description: Mapped[str] = mapped_column(Text, deferred=True)
    # offered_item_category => should be choice
    desired_offer: Mapped[str] = mapped_column(nullable=True, default="contractual")
    status: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
