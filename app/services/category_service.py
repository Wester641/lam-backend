from typing import List, Optional
from sqlalchemy.orm import Session
from slugify import slugify
from app.database.models import Category
from app.repositories.category import CategoryRepository
from app.schemas import CategoryCreate, CategoryUpdate
from .base import BaseService

class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate, CategoryRepository]):
    def __init__(self, db: Session):
        repository = CategoryRepository(db)
        super().__init__(repository)
        self.db = db
    
    def validate_create(self, obj_in: CategoryCreate) -> bool:
        """Валидация перед созданием категории"""
        # Проверяем уникальность имени
        if self.repository.get_by_slug(obj_in.slug):
            raise ValueError(f"Категория с slug '{obj_in.slug}' уже существует")
        
        # Проверяем существование родительской категории
        if obj_in.parent_id:
            parent = self.repository.get_by_id(obj_in.parent_id)
            if not parent:
                raise ValueError(f"Родительская категория с ID {obj_in.parent_id} не найдена")
        
        return True
    
    def validate_update(self, id: int, obj_in: CategoryUpdate) -> bool:
        """Валидация перед обновлением категории"""
        # Проверяем существование категории
        category = self.repository.get_by_id(id)
        if not category:
            raise ValueError(f"Категория с ID {id} не найдена")
        
        # Проверяем уникальность slug при обновлении
        if obj_in.slug:
            existing = self.repository.get_by_slug(obj_in.slug)
            if existing and existing.id != id:
                raise ValueError(f"Категория с slug '{obj_in.slug}' уже существует")
        
        # Проверяем родительскую категорию
        if obj_in.parent_id:
            parent = self.repository.get_by_id(obj_in.parent_id)
            if not parent:
                raise ValueError(f"Родительская категория с ID {obj_in.parent_id} не найдена")
            
            # Проверяем, что категория не становится родителем самой себя
            if obj_in.parent_id == id:
                raise ValueError("Категория не может быть родителем самой себя")
        
        return True
    
    def create(self, obj_in: CategoryCreate) -> Category:
        """Создать категорию с валидацией"""
        # Автоматически генерируем slug если не задан
        create_data = obj_in.dict()
        if not create_data.get('slug'):
            create_data['slug'] = slugify(obj_in.name)
        
        # Создаем новый объект с обновленными данными
        updated_obj = CategoryCreate(**create_data)
        
        self.validate_create(updated_obj)
        return self.repository.create(updated_obj)
    
    def update(self, id: int, obj_in: CategoryUpdate) -> Optional[Category]:
        """Обновить категорию с валидацией"""
        self.validate_update(id, obj_in)
        
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            return None
        
        # Автоматически обновляем slug если изменилось имя
        if obj_in.name and not obj_in.slug:
            obj_in.slug = slugify(obj_in.name)
        
        return self.repository.update(db_obj, obj_in)
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Получить категорию по slug"""
        return self.repository.get_by_slug(slug)
    
    def get_root_categories(self) -> List[Category]:
        """Получить корневые категории"""
        return self.repository.get_root_categories()
    
    def get_category_tree(self) -> List[Category]:
        """Получить дерево категорий"""
        return self.repository.get_category_tree()
    
    def get_children(self, parent_id: int) -> List[Category]:
        """Получить дочерние категории"""
        return self.repository.get_children(parent_id)
    
    def search_by_name(self, name: str) -> List[Category]:
        """Поиск категорий по имени"""
        return self.repository.search_by_name(name)
    
    def delete(self, id: int) -> bool:
        """Удалить категорию с проверкой зависимостей"""
        category = self.repository.get_by_id(id)
        if not category:
            return False
        
        # Проверяем, есть ли дочерние категории
        children = self.get_children(id)
        if children:
            raise ValueError("Нельзя удалить категорию, у которой есть дочерние категории")
        
        # Проверяем, есть ли товары в категории
        from app.repositories.product import ProductRepository
        product_repo = ProductRepository(self.db)
        products = product_repo.get_by_category(id, limit=1)
        if products:
            raise ValueError("Нельзя удалить категорию, в которой есть товары")
        
        return self.repository.delete(id)