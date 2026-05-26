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
