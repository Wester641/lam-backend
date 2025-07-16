from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый репозиторий с общими CRUD операциями"""
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Получить объект по ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 10, active_only: bool = True) -> List[ModelType]:
        """Получить все объекты с пагинацией"""
        query = self.db.query(self.model)
        if active_only and hasattr(self.model, 'is_active'):
            query = query.filter(self.model.is_active == True)
        return query.offset(skip).limit(limit).all()
    
    def get_count(self, active_only: bool = True) -> int:
        """Получить количество объектов"""
        query = self.db.query(self.model)
        if active_only and hasattr(self.model, 'is_active'):
            query = query.filter(self.model.is_active == True)
        return query.count()
    
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Создать новый объект"""
        obj_data = obj_in.dict() if hasattr(obj_in, 'dict') else obj_in
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """Обновить существующий объект"""
        update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, 'dict') else obj_in
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """Удалить объект по ID"""
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
    
    def soft_delete(self, id: int) -> bool:
        """Мягкое удаление (установить is_active = False)"""
        db_obj = self.get_by_id(id)
        if db_obj and hasattr(db_obj, 'is_active'):
            db_obj.is_active = False
            self.db.commit()
            return True
        return False