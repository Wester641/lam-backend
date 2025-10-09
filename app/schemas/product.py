from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from .common import BaseSchema, StockState
from .category import CategoryResponse
from .brand import BrandResponse

# Tag schemas
class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    slug: str = Field(..., min_length=1, max_length=50)
    is_active: bool = True

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    slug: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None

class TagResponse(TagBase, BaseSchema):
    id: int
    created_at: datetime

# Shop schemas
class ShopBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True

class ShopCreate(ShopBase):
    pass

class ShopUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None

class ShopResponse(ShopBase, BaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# Image schemas
class ImageBase(BaseModel):
    url: str = Field(..., min_length=1, max_length=500)
    alt_text: Optional[str] = Field(None, max_length=255)
    is_primary: bool = False
    sort_order: int = 0

class ImageCreate(ImageBase):
    pass

class ImageUpdate(BaseModel):
    url: Optional[str] = Field(None, min_length=1, max_length=500)
    alt_text: Optional[str] = Field(None, max_length=255)
    is_primary: Optional[bool] = None
    sort_order: Optional[int] = None

class ImageResponse(ImageBase, BaseSchema):
    id: int
    created_at: datetime

# AttributeType schemas
class AttributeTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    slug: str = Field(..., min_length=1, max_length=50)
    input_type: str = "select"
    is_required: bool = False
    is_active: bool = True

class AttributeTypeCreate(AttributeTypeBase):
    pass

class AttributeTypeResponse(AttributeTypeBase, BaseSchema):
    id: int
    created_at: datetime

# Attribute schemas
class AttributeBase(BaseModel):
    attribute_type_id: int
    value: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    hex_color: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True

class AttributeCreate(AttributeBase):
    pass

class AttributeResponse(AttributeBase, BaseSchema):
    id: int
    created_at: datetime
    attribute_type: AttributeTypeResponse

# ProductVariant schemas
class ProductVariantBase(BaseModel):
    attribute_id: int
    price_modifier: float = 0.0
    stock_quantity: int = 0
    sku_suffix: Optional[str] = Field(None, max_length=20)
    is_active: bool = True

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantResponse(ProductVariantBase, BaseSchema):
    id: int
    product_id: int
    created_at: datetime
    attribute: AttributeResponse

# Product schemas
class ProductBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    short_description: Optional[str] = None
    sku: Optional[str] = Field(None)
    base_price: float = Field(..., gt=0)
    old_price: Optional[float] = Field(None, gt=0)
    stock_state: StockState = StockState.AVAILABLE
    total_stock: int = Field(default=0, ge=0)
    min_order_quantity: int = Field(default=1, ge=1)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    shop_id: Optional[int] = None
    is_active: bool = True
    is_featured: bool = False

class ProductCreate(ProductBase):
    tag_ids: List[int] = []
    image_ids: List[int] = []
    
    shop_name: Optional[str] = "L&M Zone"
    delivered_by: str = "Aug 02"
    specifications: Dict[str, List[str]] = Field(
        default_factory=lambda: {"spec_images": []},
        description="Спецификации товара с изображениями"
    )
    colors: List[str] = Field(
        default_factory=list,
        description="Доступные цвета товара"
    )
    tags_names: List[str] = Field(
        default=[],
        description="Теги по именам (альтернатива tag_ids)"
    )
    
    rating: Optional[str] = "3.8"
    reviewCount: Optional[str] = "0"

class ProductUpdate(BaseModel):
    # Основные поля
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    short_description: Optional[str] = None
    sku: Optional[str] = Field(None)
    base_price: Optional[float] = Field(None, gt=0)
    old_price: Optional[float] = Field(None, gt=0)
    stock_state: Optional[StockState] = None
    total_stock: Optional[int] = Field(None, ge=0)
    min_order_quantity: Optional[int] = Field(None, ge=1)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    shop_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    
    tag_ids: Optional[List[int]] = None
    image_ids: Optional[List[int]] = None
    
    shop_name: Optional[str] = None
    delivered_by: Optional[str] = None
    specifications: Optional[Dict[str, List[str]]] = None
    colors: Optional[List[str]] = None
    tags_names: Optional[List[str]] = None
    rating: Optional[str] = None
    reviewCount: Optional[str] = None

class ProductResponse(ProductBase, BaseSchema):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None
    shop: Optional[ShopResponse] = None
    tags: List[TagResponse] = []
    images: List[ImageResponse] = []
    variants: List[ProductVariantResponse] = []
    
    rating: str = "0.0"
    reviewCount: str = "0"
    shop_name: str = "L&M Zone"
    price: float = 0.0
    old_price_formatted: str = ""  
    new_price_formatted: str = ""  
    image: str = "" 
    delivered_by: str = "Aug 02"
    discount: str = "" 
    specifications: Dict[str, List[str]] = Field(default_factory=lambda: {"spec_images": []})
    colors: List[str] = Field(default_factory=list)
    tags_names: List[str] = Field(default_factory=list) 
    
    review_count: int = 0
    discount_percentage: Optional[float] = None
    new_price: float = 0.0
    
    @validator('price', always=True)
    def set_price_from_base_price(cls, v, values):
        return values.get('base_price', 0)
    
    @validator('new_price', always=True)
    def calculate_new_price(cls, v, values):
        return values.get('base_price', 0)
    
    @validator('discount_percentage', always=True)
    def calculate_discount(cls, v, values):
        old_price = values.get('old_price')
        base_price = values.get('base_price')
        if old_price and base_price and old_price > base_price:
            return round(((old_price - base_price) / old_price) * 100, 1)
        return None
    
    @validator('old_price_formatted', always=True)
    def format_old_price(cls, v, values):
        old_price = values.get('old_price')
        return f"{old_price}$" if old_price else ""
    
    @validator('new_price_formatted', always=True)
    def format_new_price(cls, v, values):
        base_price = values.get('base_price', 0)
        return f"{base_price}$"
    
    @validator('discount', always=True)
    def format_discount(cls, v, values):
        discount_percentage = values.get('discount_percentage')
        return f"{int(discount_percentage)}%OFF" if discount_percentage else ""

# Simplified product response for listings
class ProductListResponse(BaseSchema):
    id: int
    stock_state: str
    total_stock: int
    rating: str = "3.8"
    reviewCount: str = "0"
    title: str
    shop_name: str = "L&M Zone"
    price: float
    old_price: str = ""
    new_price: str = ""
    image: str = ""
    delivered_by: str = ""
    discount: str = ""
    sku: str
    description: str = ""
    specifications: Dict[str, List[str]] = Field(default_factory=lambda: {"spec_images": []})
    colors: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    slug: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None
    shop: Optional[ShopResponse] = None
    created_at: Optional[datetime] = None