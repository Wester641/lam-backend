from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from app.database.models import Product, Category, Brand, Tag, Image, ProductVariant
from app.schemas import ProductCreate, ProductUpdate
from .base import BaseRepository

class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    def __init__(self, db: Session):
        super().__init__(Product, db)
    
    def get_by_id_with_relations(self, id: int) -> Optional[Product]:
        """Получить товар со всеми связанными данными"""
        return self.db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.brand),
            joinedload(Product.shop),
            joinedload(Product.tags),
            joinedload(Product.images),
            joinedload(Product.variants).joinedload(ProductVariant.attribute)
        ).filter(Product.id == id).first()
    
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """Получить товар по slug"""
        return self.db.query(Product).filter(Product.slug == slug).first()
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Получить товар по SKU"""
        return self.db.query(Product).filter(Product.sku == sku).first()
    
    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 10) -> List[Product]:
        """Получить товары по категории"""
        return self.db.query(Product).filter(
            and_(
                Product.category_id == category_id,
                Product.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_brand(self, brand_id: int, skip: int = 0, limit: int = 10) -> List[Product]:
        """Получить товары по бренду"""
        return self.db.query(Product).filter(
            and_(
                Product.brand_id == brand_id,
                Product.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_featured(self, limit: int = 10) -> List[Product]:
        """Получить рекомендуемые товары"""
        return self.db.query(Product).filter(
            and_(
                Product.is_featured == True,
                Product.is_active == True
            )
        ).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 10) -> List[Product]:
        """Поиск товаров по названию и описанию"""
        search_filter = or_(
            Product.title.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%"),
            Product.sku.ilike(f"%{query}%")
        )
        
        return self.db.query(Product).filter(
            and_(search_filter, Product.is_active == True)
        ).offset(skip).limit(limit).all()
    
    def filter_products(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10) -> List[Product]:
        """Фильтрация товаров по различным параметрам"""
        query = self.db.query(Product).filter(Product.is_active == True)
        
        # Фильтр по категории
        if 'category_id' in filters:
            query = query.filter(Product.category_id == filters['category_id'])
        
        # Фильтр по бренду
        if 'brand_id' in filters:
            query = query.filter(Product.brand_id == filters['brand_id'])
        
        # Фильтр по цене
        if 'min_price' in filters:
            query = query.filter(Product.base_price >= filters['min_price'])
        if 'max_price' in filters:
            query = query.filter(Product.base_price <= filters['max_price'])
        
        # Фильтр по наличию
        if 'in_stock' in filters and filters['in_stock']:
            query = query.filter(Product.total_stock > 0)
        
        # Фильтр по состоянию
        if 'stock_state' in filters:
            query = query.filter(Product.stock_state == filters['stock_state'])
        
        # Сортировка
        sort_by = filters.get('sort_by', 'created_at')
        sort_order = filters.get('sort_order', 'desc')
        
        if hasattr(Product, sort_by):
            order_field = getattr(Product, sort_by)
            if sort_order == 'desc':
                query = query.order_by(desc(order_field))
            else:
                query = query.order_by(order_field)
        
        return query.offset(skip).limit(limit).all()
    
    def create_with_relations(self, obj_in: ProductCreate) -> Product:
        """Создать товар со связанными данными"""
        # Извлекаем связанные данные
        tag_ids = obj_in.tag_ids if hasattr(obj_in, 'tag_ids') else []
        image_ids = obj_in.image_ids if hasattr(obj_in, 'image_ids') else []
        
        # Создаем основной объект товара
        product_data = obj_in.dict(exclude={'tag_ids', 'image_ids'})
        db_product = Product(**product_data)
        
        # Добавляем теги
        if tag_ids:
            tags = self.db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
            db_product.tags = tags
        
        # Добавляем изображения
        if image_ids:
            images = self.db.query(Image).filter(Image.id.in_(image_ids)).all()
            db_product.images = images
        
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def update_with_relations(self, db_obj: Product, obj_in: ProductUpdate) -> Product:
        """Обновить товар со связанными данными"""
        # Обновляем основные поля
        update_data = obj_in.dict(exclude_unset=True, exclude={'tag_ids', 'image_ids'})
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        # Обновляем теги
        if hasattr(obj_in, 'tag_ids') and obj_in.tag_ids is not None:
            tags = self.db.query(Tag).filter(Tag.id.in_(obj_in.tag_ids)).all()
            db_obj.tags = tags
        
        # Обновляем изображения
        if hasattr(obj_in, 'image_ids') and obj_in.image_ids is not None:
            images = self.db.query(Image).filter(Image.id.in_(obj_in.image_ids)).all()
            db_obj.images = images
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj