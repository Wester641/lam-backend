from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.brand_service import BrandService
from app.schemas import BrandCreate, BrandUpdate, BrandResponse

router = APIRouter()

@router.get("/", response_model=List[BrandResponse])
def get_brands(
    skip: int = 0,
    limit: int = 10,
    search: str = Query(None, description="Поиск по названию бренда"),
    db: Session = Depends(get_db)
):
    """Получить список брендов"""
    brand_service = BrandService(db)
    
    if search:
        brands = brand_service.search_by_name(search)
        return brands[skip:skip + limit]
    
    brands = brand_service.get_all(skip=skip, limit=limit)
    return brands

@router.get("/popular", response_model=List[BrandResponse])
def get_popular_brands(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получить популярные бренды"""
    brand_service = BrandService(db)
    return brand_service.get_popular_brands(limit)

@router.get("/{brand_id}", response_model=BrandResponse)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    """Получить бренд по ID"""
    brand_service = BrandService(db)
    brand = brand_service.get_by_id(brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бренд не найден"
        )
    return brand

@router.get("/slug/{slug}", response_model=BrandResponse)
def get_brand_by_slug(slug: str, db: Session = Depends(get_db)):
    """Получить бренд по slug"""
    brand_service = BrandService(db)
    brand = brand_service.get_by_slug(slug)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бренд не найден"
        )
    return brand

@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
def create_brand(
    brand: BrandCreate,
    db: Session = Depends(get_db)
):
    """Создать новый бренд"""
    brand_service = BrandService(db)
    try:
        return brand_service.create(brand)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{brand_id}", response_model=BrandResponse)
def update_brand(
    brand_id: int,
    brand_update: BrandUpdate,
    db: Session = Depends(get_db)
):
    """Обновить бренд"""
    brand_service = BrandService(db)
    try:
        updated_brand = brand_service.update(brand_id, brand_update)
        if not updated_brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бренд не найден"
            )
        return updated_brand
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    """Удалить бренд"""
    brand_service = BrandService(db)
    try:
        success = brand_service.delete(brand_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бренд не найден"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )