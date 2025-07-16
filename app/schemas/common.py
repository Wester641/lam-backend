from pydantic import BaseModel, Field
from typing import List, Any
from enum import Enum

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class StockState(str, Enum):
    AVAILABLE = "Available"
    OUT_OF_STOCK = "OutOfStock"
    DISCONTINUED = "Discontinued"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class InputType(str, Enum):
    SELECT = "select"
    TEXT = "text"
    NUMBER = "number"
    COLOR = "color"

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int