from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

# Association tables for many-to-many relationships
product_tags = Table(
    'product_tags',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

product_images = Table(
    'product_images',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships (исправленные)
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent", overlaps="parent")
    products = relationship("Product", back_populates="category")

class Brand(Base):
    __tablename__ = 'brands'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    logo_url = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="brand")

class AttributeType(Base):
    __tablename__ = 'attribute_types'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)  # Color, Size, Memory, Storage
    slug = Column(String(50), nullable=False, unique=True)
    input_type = Column(String(20), default='select')  # select, text, number, color
    is_required = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    attributes = relationship("Attribute", back_populates="attribute_type")

class Attribute(Base):
    __tablename__ = 'attributes'
    
    id = Column(Integer, primary_key=True, index=True)
    attribute_type_id = Column(Integer, ForeignKey('attribute_types.id'), nullable=False)
    value = Column(String(100), nullable=False)  # "Midnight", "13-inch", "8GB", "256GB"
    slug = Column(String(100), nullable=False)
    hex_color = Column(String(7))  # For color attributes
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    attribute_type = relationship("AttributeType", back_populates="attributes")
    product_variants = relationship("ProductVariant", back_populates="attribute")

class Shop(Base):
    __tablename__ = 'shops'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="shop")

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    short_description = Column(Text)
    sku = Column(String(50), nullable=False, unique=True)
    
    # Basic product info
    base_price = Column(Float, nullable=False)
    old_price = Column(Float)
    
    # Stock and availability
    stock_state = Column(String(20), default='Available')  # Available, OutOfStock, Discontinued
    total_stock = Column(Integer, default=0)
    min_order_quantity = Column(Integer, default=1)
    
    # SEO and metadata
    meta_title = Column(String(255))
    meta_description = Column(Text)
    
    # Relationships
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=True)
    
    # Product status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    shop = relationship("Shop", back_populates="products")
    tags = relationship("Tag", secondary=product_tags, back_populates="products")
    images = relationship("Image", secondary=product_images, back_populates="products")
    variants = relationship("ProductVariant", back_populates="product")
    reviews = relationship("Review", back_populates="product")

class ProductVariant(Base):
    __tablename__ = 'product_variants'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    attribute_id = Column(Integer, ForeignKey('attributes.id'), nullable=False)
    
    # Variant-specific pricing and stock
    price_modifier = Column(Float, default=0.0)  # Additional price for this variant
    stock_quantity = Column(Integer, default=0)
    sku_suffix = Column(String(20))  # To create unique SKU for variant
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="variants")
    attribute = relationship("Attribute", back_populates="product_variants")

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    slug = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    products = relationship("Product", secondary=product_tags, back_populates="tags")

class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    products = relationship("Product", secondary=product_images, back_populates="images")

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(255))
    rating = Column(Float, nullable=False)
    title = Column(String(255))
    comment = Column(Text)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="reviews")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), nullable=False, unique=True)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20))
    
    # Order details
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default='pending')  # pending, confirmed, processing, shipped, delivered, cancelled
    notes = Column(Text)
    
    # Delivery info
    delivery_address = Column(Text)
    delivery_date = Column(DateTime)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Selected variant attributes (stored as JSON)
    variant_attributes = Column(JSON)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")