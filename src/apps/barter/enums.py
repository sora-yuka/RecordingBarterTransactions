from enum import Enum


class ItemCategory(Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FURNITURE = "furniture"
    BOOKS = "books"
    VEHICLES = "vehicles"
    OTHER = "other"


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"


class BarterStatus(Enum):
    ACTIVE = "active"
    EXCHANGED = "exchanged"
    DELETED = "deleted"


class DealStatus(Enum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELED = "canceled"
