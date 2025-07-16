from fastapi import APIRouter
from app.api.v1.endpoints import categories, brands, products

api_router = APIRouter()

api_router.include_router(
    categories.router,
    prefix="/categories",
    tags=["categories"]
)

api_router.include_router(
    brands.router,
    prefix="/brands", 
    tags=["brands"]
)

api_router.include_router(
    products.router,
    prefix="/products",
    tags=["products"]
)