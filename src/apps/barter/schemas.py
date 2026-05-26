from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, computed_field

from src.apps.barter.enums import ItemCategory, MediaType, BarterStatus, DealStatus


class BaseBarterMedia(BaseModel):
    file_path: str = Field(max_length=500)
    media_type: MediaType
    order: int = Field(default=0, ge=0)


class CreateBarterMediaSchema(BaseBarterMedia):
    pass


class ReadBarterMediaSchema(BaseBarterMedia):
    model_config = ConfigDict(from_attributes=True)

    id: int
    barter_id: int


class BaseBarter(BaseModel):
    offered_title: str = Field(max_length=150)
    offered_description: str
    offered_item_category: ItemCategory
    desired_offer: str | None = Field(default=None, max_length=300)


class CreateBarterSchema(BaseBarter):
    pass


class UpdateBarterSchema(BaseBarter):
    offered_title: str | None = Field(default=None, max_length=150)
    offered_description: str | None = None
    offered_item_category: ItemCategory | None = None
    desired_offer: str | None = Field(default=None, max_length=300)
    status: BarterStatus | None = None


class ReadBarterSchema(BaseBarter):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    status: BarterStatus
    offered_item_media: list[ReadBarterMediaSchema] = []
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def desired_offer_display(self) -> str:
        return self.desired_offer or "Contractual"


class CreateBarterDealSchema(BaseModel):
    # chat_id needed
    initiator_id: int
    responder_id: int


class UpdateBarterDealStatusSchema(BaseModel):
    status: DealStatus


class ReadBarterDealSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    initiator_id: int
    responser_id: int
    initiator_barter_id: int
    responder_barter_id: int
    status: DealStatus
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None


class ReadBarterDealDetailSchema(ReadBarterDealSchema):
    initiator_barter: ReadBarterSchema | None = None
    responder_barter: ReadBarterSchema | None = None
