from typing import List, Optional
from sqlalchemy.orm import Session
from slugify import slugify
from app.database.models import Brand
from app.repositories.brand import BrandRepository
from app.schemas import BrandCreate, BrandUpdate
from .base import BaseService

class BrandService(BaseService[Brand, BrandCreate, BrandUpdate, BrandRepository]):
    def __init__(self, db: Session):
        repository = BrandRepository(db)
        super().__init__(repository)
        self.db = db
    
    def validate_create(self, obj_in: BrandCreate) -> bool:
        """Валидация перед созданием бренда"""
        # Проверяем уникальность slug
        if self.repository.get_by_slug(obj_in.slug):
            raise ValueError(f"Бренд с slug '{obj_in.slug}' уже существует")
        
        return True
    
    def validate_update(self, id: int, obj_in: BrandUpdate) -> bool:
        """Валидация перед обновлением бренда"""
        # Проверяем существование бренда
        brand = self.repository.get_by_id(id)
        if not brand:
            raise ValueError(f"Бренд с ID {id} не найден")
        
        # Проверяем уникальность slug при обновлении
        if obj_in.slug:
            existing = self.repository.get_by_slug(obj_in.slug)
            if existing and existing.id != id:
                raise ValueError(f"Бренд с slug '{obj_in.slug}' уже существует")
        
        return True
    
    def create(self, obj_in: BrandCreate) -> Brand:
        """Создать бренд с валидацией"""
        # Автоматически генерируем slug если не задан
        create_data = obj_in.dict()
        if not create_data.get('slug'):
            create_data['slug'] = slugify(obj_in.name)
        
        # Создаем новый объект с обновленными данными
        updated_obj = BrandCreate(**create_data)
        
        self.validate_create(updated_obj)
        return self.repository.create(updated_obj)
    
    def update(self, id: int, obj_in: BrandUpdate) -> Optional[Brand]:
        """Обновить бренд с валидацией"""
        self.validate_update(id, obj_in)
        
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            return None
        
        # Автоматически обновляем slug если изменилось имя
        if obj_in.name and not obj_in.slug:
            obj_in.slug = slugify(obj_in.name)
        
        return self.repository.update(db_obj, obj_in)
    
    def get_by_slug(self, slug: str) -> Optional[Brand]:
        """Получить бренд по slug"""
        return self.repository.get_by_slug(slug)
    
    def search_by_name(self, name: str) -> List[Brand]:
        """Поиск брендов по имени"""
        return self.repository.search_by_name(name)
    
    def get_popular_brands(self, limit: int = 10) -> List[Brand]:
        """Получить популярные бренды"""
        return self.repository.get_popular_brands(limit)
    
    def delete(self, id: int) -> bool:
        """Удалить бренд с проверкой зависимостей"""
        brand = self.repository.get_by_id(id)
        if not brand:
            return False
        
        # Проверяем, есть ли товары этого бренда
        from app.repositories.product import ProductRepository
        product_repo = ProductRepository(self.db)
        products = product_repo.get_by_brand(id, limit=1)
        if products:
            raise ValueError("Нельзя удалить бренд, у которого есть товары")
        
        return self.repository.delete(id)