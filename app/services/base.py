from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Type, TypeVar, Generic
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)

class BaseService(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, RepositoryType]):
    """Базовый сервис с бизнес-логикой"""
    
    def __init__(self, repository: RepositoryType):
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Получить объект по ID"""
        return self.repository.get_by_id(id)
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[ModelType]:
        """Получить все объекты"""
        return self.repository.get_all(skip=skip, limit=limit)
    
    def get_count(self) -> int:
        """Получить количество объектов"""
        return self.repository.get_count()
    
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Создать новый объект"""
        # Здесь можно добавить валидацию, обработку данных и т.д.
        return self.repository.create(obj_in)
    
    def update(self, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """Обновить объект"""
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            return None
        return self.repository.update(db_obj, obj_in)
    
    def delete(self, id: int) -> bool:
        """Удалить объект"""
        return self.repository.delete(id)
    
    def soft_delete(self, id: int) -> bool:
        """Мягкое удаление"""
        return self.repository.soft_delete(id)
    
    @abstractmethod
    def validate_create(self, obj_in: CreateSchemaType) -> bool:
        """Валидация перед созданием"""
        pass
    
    @abstractmethod
    def validate_update(self, id: int, obj_in: UpdateSchemaType) -> bool:
        """Валидация перед обновлением"""
        pass