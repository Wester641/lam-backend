from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .common import BaseSchema

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)  # Сделали опциональным
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase, BaseSchema):
    id: int
    slug: str  # В ответе slug обязательный
    created_at: datetime
    updated_at: datetime
    children: List['CategoryResponse'] = []

# Update forward references
CategoryResponse.model_rebuild()