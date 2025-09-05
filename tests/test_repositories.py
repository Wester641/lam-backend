import sys
import os

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.repositories import CategoryRepository, BrandRepository
from app.schemas import CategoryCreate, BrandCreate
from slugify import slugify


def test_repositories():
    db = SessionLocal()

    try:
        print("🧪 Тестирование репозиториев...")

        # Тест CategoryRepository
        print("\n📁 Тестирование CategoryRepository:")
        category_repo = CategoryRepository(db)

        # Создаем тестовую категорию
        test_category = CategoryCreate(
            name="Ноутбуки",
            slug=slugify("Ноутбуки"),
            description="Категория ноутбуков",
            is_active=True,
        )

        created_category = category_repo.create(test_category)
        print(
            f"✅ Создана категория: {created_category.name} (ID: {created_category.id})"
        )

        # Получаем категорию по ID
        found_category = category_repo.get_by_id(created_category.id)
        print(f"✅ Найдена категория по ID: {found_category.name}")

        # Получаем по slug
        found_by_slug = category_repo.get_by_slug(created_category.slug)
        print(f"✅ Найдена категория по slug: {found_by_slug.name}")

        # Тест BrandRepository
        print("\n🏷️ Тестирование BrandRepository:")
        brand_repo = BrandRepository(db)

        # Создаем тестовый бренд
        test_brand = BrandCreate(
            name="Apple",
            slug=slugify("Apple"),
            description="Бренд Apple",
            is_active=True,
        )

        created_brand = brand_repo.create(test_brand)
        print(f"✅ Создан бренд: {created_brand.name} (ID: {created_brand.id})")

        # Получаем все категории и бренды
        all_categories = category_repo.get_all()
        all_brands = brand_repo.get_all()

        print(f"\n📊 Статистика:")
        print(f"📁 Всего категорий: {len(all_categories)}")
        print(f"🏷️ Всего брендов: {len(all_brands)}")

        # Показываем содержимое
        print(f"\n📋 Категории:")
        for cat in all_categories:
            print(f"  - {cat.name} ({cat.slug})")

        print(f"\n📋 Бренды:")
        for brand in all_brands:
            print(f"  - {brand.name} ({brand.slug})")

        print("\n✅ Все тесты репозиториев прошли успешно!")

    except Exception as e:
        print(f"❌ Ошибка в тестах: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_repositories()
