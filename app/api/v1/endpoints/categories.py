from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.category_service import CategoryService
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse, PaginationParams

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получить список категорий"""
    category_service = CategoryService(db)
    categories = category_service.get_all(skip=skip, limit=limit)
    return categories

@router.get("/tree", response_model=List[CategoryResponse])
def get_category_tree(db: Session = Depends(get_db)):
    """Получить дерево категорий"""
    category_service = CategoryService(db)
    return category_service.get_category_tree()

@router.get("/roots", response_model=List[CategoryResponse])
def get_root_categories(db: Session = Depends(get_db)):
    """Получить корневые категории"""
    category_service = CategoryService(db)
    return category_service.get_root_categories()

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category_service = CategoryService(db)
    category = category_service.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return category

@router.get("/slug/{slug}", response_model=CategoryResponse)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    """Получить категорию по slug"""
    category_service = CategoryService(db)
    category = category_service.get_by_slug(slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Создать новую категорию"""
    category_service = CategoryService(db)
    try:
        return category_service.create(category)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Обновить категорию"""
    category_service = CategoryService(db)
    try:
        updated_category = category_service.update(category_id, category_update)
        if not updated_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        return updated_category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию"""
    category_service = CategoryService(db)
    try:
        success = category_service.delete(category_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{category_id}/children", response_model=List[CategoryResponse])
def get_category_children(category_id: int, db: Session = Depends(get_db)):
    """Получить дочерние категории"""
    category_service = CategoryService(db)
    children = category_service.get_children(category_id)
    return children