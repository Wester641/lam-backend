from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import Category
from app.schemas import CategoryCreate, CategoryUpdate
from .base import BaseRepository

class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self, db: Session):
        super().__init__(Category, db)
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Получить категорию по slug"""
        return self.db.query(Category).filter(Category.slug == slug).first()
    
    def get_root_categories(self) -> List[Category]:
        """Получить корневые категории (без родителя)"""
        return self.db.query(Category).filter(
            and_(Category.parent_id.is_(None), Category.is_active == True)
        ).all()
    
    def get_children(self, parent_id: int) -> List[Category]:
        """Получить дочерние категории"""
        return self.db.query(Category).filter(
            and_(Category.parent_id == parent_id, Category.is_active == True)
        ).all()
    
    def get_category_tree(self) -> List[Category]:
        """Получить дерево категорий"""
        # Сначала получаем все корневые категории
        root_categories = self.get_root_categories()
        
        # Для каждой корневой категории загружаем детей
        for category in root_categories:
            category.children = self.get_children(category.id)
        
        return root_categories
    
    def search_by_name(self, name: str) -> List[Category]:
        """Поиск категорий по имени"""
        return self.db.query(Category).filter(
            and_(
                Category.name.ilike(f"%{name}%"),
                Category.is_active == True
            )
        ).all()