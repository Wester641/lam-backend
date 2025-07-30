from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from slugify import slugify
from app.database.models import Product
from app.repositories.product import ProductRepository
from app.repositories.category import CategoryRepository
from app.repositories.brand import BrandRepository
from app.schemas import ProductCreate, ProductUpdate
from .base import BaseService

class ProductService(BaseService[Product, ProductCreate, ProductUpdate, ProductRepository]):
    def __init__(self, db: Session):
        repository = ProductRepository(db)
        super().__init__(repository)
        self.db = db
        self.category_repo = CategoryRepository(db)
        self.brand_repo = BrandRepository(db)
    
    def validate_create(self, obj_in: ProductCreate) -> bool:
        """Валидация перед созданием товара"""
        # Проверяем уникальность SKU
        if self.repository.get_by_sku(obj_in.sku):
            raise ValueError(f"Товар с SKU '{obj_in.sku}' уже существует")
        
        # Проверяем уникальность slug
        if self.repository.get_by_slug(obj_in.slug):
            raise ValueError(f"Товар с slug '{obj_in.slug}' уже существует")
        
        # Проверяем существование категории
        category = self.category_repo.get_by_id(obj_in.category_id)
        if not category:
            raise ValueError(f"Категория с ID {obj_in.category_id} не найдена")
        
        # Проверяем существование бренда (если указан)
        if obj_in.brand_id:
            brand = self.brand_repo.get_by_id(obj_in.brand_id)
            if not brand:
                raise ValueError(f"Бренд с ID {obj_in.brand_id} не найден")
        
        # Проверяем цены
        if obj_in.old_price and obj_in.old_price <= obj_in.base_price:
            raise ValueError("Старая цена должна быть больше текущей цены")
        
        return True
    
    def validate_update(self, id: int, obj_in: ProductUpdate) -> bool:
        """Валидация перед обновлением товара"""
        # Проверяем существование товара
        product = self.repository.get_by_id(id)
        if not product:
            raise ValueError(f"Товар с ID {id} не найден")
        
        # Проверяем уникальность SKU при обновлении
        if obj_in.sku:
            existing = self.repository.get_by_sku(obj_in.sku)
            if existing and existing.id != id:
                raise ValueError(f"Товар с SKU '{obj_in.sku}' уже существует")
        
        # Проверяем уникальность slug при обновлении
        if obj_in.slug:
            existing = self.repository.get_by_slug(obj_in.slug)
            if existing and existing.id != id:
                raise ValueError(f"Товар с slug '{obj_in.slug}' уже существует")
        
        # Проверяем категорию
        if obj_in.category_id:
            category = self.category_repo.get_by_id(obj_in.category_id)
            if not category:
                raise ValueError(f"Категория с ID {obj_in.category_id} не найдена")
        
        # Проверяем бренд
        if obj_in.brand_id:
            brand = self.brand_repo.get_by_id(obj_in.brand_id)
            if not brand:
                raise ValueError(f"Бренд с ID {obj_in.brand_id} не найден")
        
        # Проверяем цены
        if obj_in.old_price and obj_in.base_price and obj_in.old_price <= obj_in.base_price:
            raise ValueError("Старая цена должна быть больше текущей цены")
        
        return True
    
    def create(self, obj_in: ProductCreate) -> Product:
        """Создать товар с валидацией и поддержкой новых полей"""
        create_data = obj_in.dict()
        if not create_data.get('slug'):
            create_data['slug'] = slugify(obj_in.title)
        
        excluded_fields = [
            'shop_name', 'delivered_by', 'specifications', 
            'colors', 'tags_names', 'rating', 'reviewCount'
        ]
        
        clean_data = {k: v for k, v in create_data.items() if k not in excluded_fields}
        
        updated_obj = ProductCreate(**clean_data)
        
        self.validate_create(updated_obj)
        
        product = self.repository.create_with_relations(updated_obj)
        
        if hasattr(obj_in, 'specifications') and obj_in.specifications:
            spec_images = obj_in.specifications.get('spec_images', [])
            if spec_images:
                from app.database.models import Image
                created_images = []
                for i, img_url in enumerate(spec_images):
                    existing_image = self.db.query(Image).filter(Image.url == img_url).first()
                    if not existing_image:
                        image = Image(
                            url=img_url,
                            alt_text=f"{product.title} - Image {i+1}",
                            is_primary=(i == 0),  # Первое изображение - основное
                            sort_order=i+1
                        )
                        self.db.add(image)
                        self.db.commit()
                        self.db.refresh(image)
                        created_images.append(image)
                    else:
                        created_images.append(existing_image)
                
                product.images = created_images
        
        if hasattr(obj_in, 'tags_names') and obj_in.tags_names:
            from app.database.models import Tag
            created_tags = []
            for tag_name in obj_in.tags_names:
                existing_tag = self.db.query(Tag).filter(Tag.name == tag_name).first()
                if not existing_tag:
                    tag = Tag(
                        name=tag_name,
                        slug=slugify(tag_name)
                    )
                    self.db.add(tag)
                    self.db.commit()
                    self.db.refresh(tag)
                    created_tags.append(tag)
                else:
                    created_tags.append(existing_tag)
            
            product.tags = created_tags
        
        if hasattr(obj_in, 'colors') and obj_in.colors:
            from app.database.models import AttributeType, Attribute, ProductVariant
            
            color_attr_type = self.db.query(AttributeType).filter(
                AttributeType.name == "Color"
            ).first()
            
            if not color_attr_type:
                color_attr_type = AttributeType(
                    name="Color",
                    slug="color",
                    input_type="select"
                )
                self.db.add(color_attr_type)
                self.db.commit()
                self.db.refresh(color_attr_type)
            
            for color in obj_in.colors:
                existing_color = self.db.query(Attribute).filter(
                    and_(
                        Attribute.attribute_type_id == color_attr_type.id,
                        Attribute.value == color
                    )
                ).first()
                
                if not existing_color:
                    color_attr = Attribute(
                        attribute_type_id=color_attr_type.id,
                        value=color,
                        slug=slugify(color)
                    )
                    self.db.add(color_attr)
                    self.db.commit()
                    self.db.refresh(color_attr)
                else:
                    color_attr = existing_color
                
                variant = ProductVariant(
                    product_id=product.id,
                    attribute_id=color_attr.id,
                    price_modifier=0,
                    stock_quantity=product.total_stock
                )
                self.db.add(variant)
            
            self.db.commit()
        
        self.db.refresh(product)
        return product
    
    def update(self, id: int, obj_in: ProductUpdate) -> Optional[Product]:
        """Обновить товар с валидацией"""
        self.validate_update(id, obj_in)
        
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            return None
        
        if obj_in.title and not obj_in.slug:
            obj_in.slug = slugify(obj_in.title)
        
        return self.repository.update_with_relations(db_obj, obj_in)
    
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """Получить товар по slug"""
        return self.repository.get_by_slug(slug)
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Получить товар по SKU"""
        return self.repository.get_by_sku(sku)
    
    def get_by_id_with_relations(self, id: int) -> Optional[Product]:
        """Получить товар со всеми связанными данными"""
        return self.repository.get_by_id_with_relations(id)
    
    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 10) -> List[Product]:
        """Получить товары по категории"""
        return self.repository.get_by_category(category_id, skip, limit)
    
    def get_by_brand(self, brand_id: int, skip: int = 0, limit: int = 10) -> List[Product]:
        """Получить товары по бренду"""
        return self.repository.get_by_brand(brand_id, skip, limit)
    
    def get_featured(self, limit: int = 10) -> List[Product]:
        """Получить рекомендуемые товары"""
        return self.repository.get_featured(limit)
    
    def search(self, query: str, skip: int = 0, limit: int = 10) -> List[Product]:
        """Поиск товаров"""
        return self.repository.search(query, skip, limit)
    
    def filter_products(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10) -> List[Product]:
        """Фильтрация товаров"""
        return self.repository.filter_products(filters, skip, limit)
    
    def update_stock(self, id: int, quantity: int) -> Optional[Product]:
        """Обновить остаток товара"""
        product = self.repository.get_by_id(id)
        if not product:
            return None
        
        product.total_stock = quantity
        
        # Обновляем состояние товара
        if quantity <= 0:
            product.stock_state = "OutOfStock"
        else:
            product.stock_state = "Available"
        
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def decrease_stock(self, id: int, quantity: int) -> Optional[Product]:
        """Уменьшить остаток товара"""
        product = self.repository.get_by_id(id)
        if not product:
            return None
        
        if product.total_stock < quantity:
            raise ValueError("Недостаточно товара на складе")
        
        return self.update_stock(id, product.total_stock - quantity)
    
    def increase_stock(self, id: int, quantity: int) -> Optional[Product]:
        """Увеличить остаток товара"""
        product = self.repository.get_by_id(id)
        if not product:
            return None
        
        return self.update_stock(id, product.total_stock + quantity)