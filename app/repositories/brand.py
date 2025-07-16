from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import Brand
from app.schemas import BrandCreate, BrandUpdate
from .base import BaseRepository

class BrandRepository(BaseRepository[Brand, BrandCreate, BrandUpdate]):
    def __init__(self, db: Session):
        super().__init__(Brand, db)
    
    def get_by_slug(self, slug: str) -> Optional[Brand]:
        """Получить бренд по slug"""
        return self.db.query(Brand).filter(Brand.slug == slug).first()
    
    def search_by_name(self, name: str) -> List[Brand]:
        """Поиск брендов по имени"""
        return self.db.query(Brand).filter(
            and_(
                Brand.name.ilike(f"%{name}%"),
                Brand.is_active == True
            )
        ).all()
    
    def get_popular_brands(self, limit: int = 10) -> List[Brand]:
        """Получить популярные бренды (с наибольшим количеством товаров)"""
        from app.database.models import Product
        
        return self.db.query(Brand).join(Product).filter(
            and_(Brand.is_active == True, Product.is_active == True)
        ).group_by(Brand.id).order_by(
            func.count(Product.id).desc()
        ).limit(limit).all()