import sys
import os

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.services import CategoryService, BrandService, ProductService
from app.schemas import CategoryCreate, BrandCreate, ProductCreate


def test_services():
    db = SessionLocal()

    try:
        print("🧪 Тестирование сервисов...")

        # Тест CategoryService
        print("\n📁 Тестирование CategoryService:")
        category_service = CategoryService(db)

        # Создаем категорию
        category_data = CategoryCreate(
            name="Смартфоны",
            description="Категория смартфонов",
            # slug будет сгенерирован автоматически
        )

        created_category = category_service.create(category_data)
        print(
            f"✅ Создана категория: {created_category.name} (slug: {created_category.slug})"
        )

        # Тест BrandService
        print("\n🏷️ Тестирование BrandService:")
        brand_service = BrandService(db)

        # Создаем бренд
        brand_data = BrandCreate(
            name="Samsung",
            description="Бренд Samsung",
            # slug будет сгенерирован автоматически
        )

        created_brand = brand_service.create(brand_data)
        print(f"✅ Создан бренд: {created_brand.name} (slug: {created_brand.slug})")

        # Тест ProductService
        print("\n📱 Тестирование ProductService:")
        product_service = ProductService(db)

        # Создаем товар
        product_data = ProductCreate(
            title="Samsung Galaxy S24",
            description="Флагманский смартфон Samsung",
            sku="SGS24-001",
            base_price=899.99,
            old_price=999.99,
            total_stock=10,
            category_id=created_category.id,
            brand_id=created_brand.id,
            is_featured=True,
        )

        created_product = product_service.create(product_data)
        print(f"✅ Создан товар: {created_product.title} (SKU: {created_product.sku})")
        print(
            f"   Цена: ${created_product.base_price}, Остаток: {created_product.total_stock}"
        )

        # Тестируем поиск
        print("\n🔍 Тестирование поиска:")
        search_results = product_service.search("Samsung")
        print(f"✅ Найдено товаров по запросу 'Samsung': {len(search_results)}")

        # Тестируем фильтрацию
        print("\n🔽 Тестирование фильтрации:")
        featured_products = product_service.get_featured()
        print(f"✅ Рекомендуемых товаров: {len(featured_products)}")

        # Тестируем управление складом
        print("\n📦 Тестирование управления складом:")
        # Уменьшаем остаток
        updated_product = product_service.decrease_stock(created_product.id, 3)
        print(f"✅ Остаток после продажи 3 штук: {updated_product.total_stock}")

        # Увеличиваем остаток
        updated_product = product_service.increase_stock(created_product.id, 5)
        print(f"✅ Остаток после поступления 5 штук: {updated_product.total_stock}")

        # Статистика
        print("\n📊 Итоговая статистика:")
        total_categories = category_service.get_count()
        total_brands = brand_service.get_count()
        total_products = product_service.get_count()

        print(f"📁 Всего категорий: {total_categories}")
        print(f"🏷️ Всего брендов: {total_brands}")
        print(f"📱 Всего товаров: {total_products}")

        print("\n✅ Все тесты сервисов прошли успешно!")

    except Exception as e:
        print(f"❌ Ошибка в тестах: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_services()
