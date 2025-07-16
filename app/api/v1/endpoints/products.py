from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.product_service import ProductService
from app.schemas import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse

router = APIRouter()

@router.get("/", response_model=List[ProductListResponse])
def get_products(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    brand_id: Optional[int] = Query(None, description="Фильтр по бренду"),
    search: Optional[str] = Query(None, description="Поиск по названию"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    in_stock: Optional[bool] = Query(None, description="Только в наличии"),
    featured: Optional[bool] = Query(None, description="Только рекомендуемые"),
    sort_by: str = Query("created_at", description="Сортировка"),
    sort_order: str = Query("desc", description="Порядок сортировки"),
    db: Session = Depends(get_db)
):
    """Получить список товаров с фильтрацией"""
    product_service = ProductService(db)
    
    # Если указан поиск
    if search:
        products = product_service.search(search, skip, limit)
        return products
    
    # Если нужны только рекомендуемые
    if featured:
        products = product_service.get_featured(limit)
        return products[skip:skip + limit]
    
    # Фильтрация
    filters = {}
    if category_id:
        filters['category_id'] = category_id
    if brand_id:
        filters['brand_id'] = brand_id
    if min_price:
        filters['min_price'] = min_price
    if max_price:
        filters['max_price'] = max_price
    if in_stock is not None:
        filters['in_stock'] = in_stock
    
    filters['sort_by'] = sort_by
    filters['sort_order'] = sort_order
    
    products = product_service.filter_products(filters, skip, limit)
    return products

@router.get("/featured", response_model=List[ProductListResponse])
def get_featured_products(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получить рекомендуемые товары"""
    product_service = ProductService(db)
    return product_service.get_featured(limit)

@router.get("/search", response_model=List[ProductListResponse])
def search_products(
    q: str = Query(..., description="Поисковый запрос"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Поиск товаров"""
    product_service = ProductService(db)
    return product_service.search(q, skip, limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получить товар по ID со всеми данными"""
    product_service = ProductService(db)
    product = product_service.get_by_id_with_relations(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    return product

@router.get("/slug/{slug}", response_model=ProductResponse)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    """Получить товар по slug"""
    product_service = ProductService(db)
    product = product_service.get_by_slug(slug)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    return product

@router.get("/sku/{sku}", response_model=ProductResponse)
def get_product_by_sku(sku: str, db: Session = Depends(get_db)):
    """Получить товар по SKU"""
    product_service = ProductService(db)
    product = product_service.get_by_sku(sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Создать новый товар"""
    product_service = ProductService(db)
    try:
        return product_service.create(product)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Обновить товар"""
    product_service = ProductService(db)
    try:
        updated_product = product_service.update(product_id, product_update)
        if not updated_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )
        return updated_product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Удалить товар"""
    product_service = ProductService(db)
    success = product_service.delete(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

@router.patch("/{product_id}/stock", response_model=ProductResponse)
def update_product_stock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    """Обновить остаток товара"""
    product_service = ProductService(db)
    try:
        updated_product = product_service.update_stock(product_id, quantity)
        if not updated_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )
        return updated_product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )