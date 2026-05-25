from pydantic import BaseModel, ConfigDict


class BaseBarterSchema(BaseModel):
    owner_id: int
    offered_title: str
    offered_item_media: list
    offered_description: str
    desired_offer: str
    status: bool  # active/inactive barter


