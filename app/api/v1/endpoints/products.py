from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.product_service import ProductService
from app.schemas import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse

router = APIRouter()

@router.get("/")
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
    """Получить список товаров в формате фронтенда"""
    product_service = ProductService(db)
    
    # Если указан поиск
    if search:
        products = product_service.search(search, skip, limit)
    elif featured:
        # Если нужны только рекомендуемые
        products = product_service.get_featured(limit)
        products = products[skip:skip + limit]
    else:
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
    
    # Преобразуем каждый продукт в формат фронтенда
    result = []
    for product in products:
        # Загружаем полную информацию
        full_product = product_service.get_by_id_with_relations(product.id)
        if not full_product:
            continue
            
        # Получаем основное изображение
        image = ""
        spec_images = []
        if full_product.images:
            for img in full_product.images:
                if img.is_primary:
                    image = img.url
                spec_images.append(img.url)
            if not image and spec_images:
                image = spec_images[0]
        
        # Получаем теги
        tags = [tag.name for tag in full_product.tags] if full_product.tags else []
        
        # Получаем цвета (пока заглушка)
        colors = ["Default"]
        
        # Вычисляем скидку
        discount = ""
        if full_product.old_price and full_product.old_price > full_product.base_price:
            discount_percent = round(((full_product.old_price - full_product.base_price) / full_product.old_price) * 100)
            discount = f"{discount_percent}%OFF"
        
        # Название магазина
        shop_name = "L&M Zone"
        if full_product.shop:
            shop_name = full_product.shop.name
        
        # Формируем ответ в формате мока
        product_data = {
            "id": full_product.id,
            "stock_state": full_product.stock_state,
            "total_stock": full_product.total_stock,
            "rating": "3.8",
            "reviewCount": "0",
            "title": full_product.title,
            "shop_name": shop_name,
            "price": full_product.base_price,
            "old_price": f"{full_product.old_price}$" if full_product.old_price else "",
            "new_price": f"{full_product.base_price}$",
            "image": image,
            "delivered_by": "Aug 02",
            "discount": discount,
            "sku": full_product.sku,
            "description": full_product.description or "",
            "specifications": {
                "spec_images": spec_images
            },
            "colors": colors,
            "tags": tags
        }
        
        result.append(product_data)
    
    return result

@router.get("/featured")
def get_featured_products(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получить рекомендуемые товары в формате фронтенда"""
    product_service = ProductService(db)
    products = product_service.get_featured(limit)
    
    result = []
    for product in products:
        full_product = product_service.get_by_id_with_relations(product.id)
        if not full_product:
            continue
            
        # Тот же код преобразования что и выше
        image = ""
        spec_images = []
        if full_product.images:
            for img in full_product.images:
                if img.is_primary:
                    image = img.url
                spec_images.append(img.url)
            if not image and spec_images:
                image = spec_images[0]
        
        tags = [tag.name for tag in full_product.tags] if full_product.tags else []
        colors = ["Default"]
        
        discount = ""
        if full_product.old_price and full_product.old_price > full_product.base_price:
            discount_percent = round(((full_product.old_price - full_product.base_price) / full_product.old_price) * 100)
            discount = f"{discount_percent}%OFF"
        
        shop_name = "L&M Zone"
        if full_product.shop:
            shop_name = full_product.shop.name
        
        product_data = {
            "id": full_product.id,
            "stock_state": full_product.stock_state,
            "total_stock": full_product.total_stock,
            "rating": "3.8",
            "reviewCount": "0",
            "title": full_product.title,
            "shop_name": shop_name,
            "price": full_product.base_price,
            "old_price": f"{full_product.old_price}$" if full_product.old_price else "",
            "new_price": f"{full_product.base_price}$",
            "image": image,
            "delivered_by": "Aug 02",
            "discount": discount,
            "sku": full_product.sku,
            "description": full_product.description or "",
            "specifications": {
                "spec_images": spec_images
            },
            "colors": colors,
            "tags": tags
        }
        
        result.append(product_data)
    
    return result

@router.get("/search")
def search_products(
    q: str = Query(..., description="Поисковый запрос"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Поиск товаров в формате фронтенда"""
    product_service = ProductService(db)
    products = product_service.search(q, skip, limit)
    
    # Преобразуем в формат фронтенда
    frontend_products = []
    for product in products:
        full_product = product_service.get_by_id_with_relations(product.id)
        if full_product:
            frontend_products.append(transform_product_for_frontend(full_product))
    
    return frontend_products

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получить товар по ID в формате фронтенда"""
    product_service = ProductService(db)
    product = product_service.get_by_id_with_relations(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    return transform_product_for_frontend(product)

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

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Создать новый товар с поддержкой всех полей мок данных"""
    product_service = ProductService(db)
    try:
        created_product = product_service.create(product)
        
        # Возвращаем в формате фронтенда
        full_product = product_service.get_by_id_with_relations(created_product.id)
        if not full_product:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении созданного товара"
            )
        
        # Преобразуем в формат мока
        image = ""
        spec_images = []
        if full_product.images:
            for img in full_product.images:
                if img.is_primary:
                    image = img.url
                spec_images.append(img.url)
            if not image and spec_images:
                image = spec_images[0]
        
        tags = [tag.name for tag in full_product.tags] if full_product.tags else []
        
        colors = []
        if full_product.variants:
            for variant in full_product.variants:
                if (variant.attribute and 
                    variant.attribute.attribute_type.name.lower() == 'color'):
                    colors.append(variant.attribute.value)
        if not colors:
            colors = ["Default"]
        
        discount = ""
        if full_product.old_price and full_product.old_price > full_product.base_price:
            discount_percent = round(((full_product.old_price - full_product.base_price) / full_product.old_price) * 100)
            discount = f"{discount_percent}%OFF"
        
        shop_name = "L&M Zone"
        if full_product.shop:
            shop_name = full_product.shop.name
        
        return {
            "id": full_product.id,
            "stock_state": full_product.stock_state,
            "total_stock": full_product.total_stock,
            "rating": "3.8",
            "reviewCount": "0",
            "title": full_product.title,
            "shop_name": shop_name,
            "price": full_product.base_price,
            "old_price": f"{full_product.old_price}$" if full_product.old_price else "",
            "new_price": f"{full_product.base_price}$",
            "image": image,
            "delivered_by": "Aug 02",
            "discount": discount,
            "sku": full_product.sku,
            "description": full_product.description or "",
            "specifications": {
                "spec_images": spec_images
            },
            "colors": colors,
            "tags": tags
        }
        
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