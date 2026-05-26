from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime, Text, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.config.database import Base
from src.apps.barter.enums import ItemCategory, MediaType, BarterStatus, DealStatus


class BarterMediaModel(Base):
    __tablename__ = "barter_media"

    id: Mapped[int] = mapped_column(primary_key=True)
    barter_id: Mapped[int] = mapped_column(ForeignKey("barters.id"))
    file_path: Mapped[str] = mapped_column(String(500))
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType))
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
    offered_item_category: Mapped[ItemCategory] = mapped_column(
        Enum(ItemCategory), nullable=False, default=ItemCategory.OTHER
    )
    desired_offer: Mapped[str | None] = mapped_column(nullable=True, default=None)
    status: Mapped[BarterStatus] = mapped_column(
        Enum(BarterStatus), default=BarterStatus.ACTIVE
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class BarterDealModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    initiator_id: Mapped[int] = mapped_column(ForeignKey("users_account.id"))
    responder_id: Mapped[int] = mapped_column(ForeignKey("users_account.id"))
    status: Mapped[DealStatus] = mapped_column(
        Enum(DealStatus), default=DealStatus.PROPOSED
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone.utc),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone.utc),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone.utc),
    )
