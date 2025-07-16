from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .common import BaseSchema

class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)  # Сделали опциональным
    logo_url: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    logo_url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class BrandResponse(BrandBase, BaseSchema):
    id: int
    slug: str  # В ответе slug обязательный
    created_at: datetime
    updated_at: datetime