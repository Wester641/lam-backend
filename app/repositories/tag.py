from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.database.models import Tag, Product
from app.schemas import TagCreate, TagUpdate
from .base import BaseRepository

class TagRepository(BaseRepository[Tag, TagCreate, TagUpdate]):
    def __init__(self, db: Session):
        super().__init__(Tag, db)
    
    def get_by_slug(self, slug: str) -> Optional[Tag]:
        """Получить тег по slug"""
        return self.db.query(Tag).filter(Tag.slug == slug).first()
    
    def get_popular_tags(self, limit: int = 20) -> List[Tag]:
        """Получить популярные теги (с наибольшим количеством товаров)"""
        return self.db.query(Tag).join(Tag.products).filter(
            and_(Tag.is_active == True, Product.is_active == True)
        ).group_by(Tag.id).order_by(
            func.count(Product.id).desc()
        ).limit(limit).all()
    
    def search_by_name(self, name: str) -> List[Tag]:
        """Поиск тегов по имени"""
        return self.db.query(Tag).filter(
            and_(
                Tag.name.ilike(f"%{name}%"),
                Tag.is_active == True
            )
        ).all()