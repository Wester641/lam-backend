import requests
import json

BASE_URL = "http://localhost:8000"


def test_api():
    print("🧪 Тестирование FastAPI эндпоинтов...")

    # 1. Проверяем корневой эндпоинт
    print("\n📍 Тестирование корневого эндпоинта:")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # 2. Проверяем health check
    print("\n❤️ Проверка здоровья:")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # 3. Получаем все категории
    print("\n📁 Получение категорий:")
    response = requests.get(f"{BASE_URL}/api/v1/categories")
    print(f"Status: {response.status_code}")
    categories = response.json()
    print(f"Найдено категорий: {len(categories)}")
    for cat in categories:
        print(f"  - {cat['name']} ({cat['slug']})")

    # 4. Получаем все бренды
    print("\n🏷️ Получение брендов:")
    response = requests.get(f"{BASE_URL}/api/v1/brands")
    print(f"Status: {response.status_code}")
    brands = response.json()
    print(f"Найдено брендов: {len(brands)}")
    for brand in brands:
        print(f"  - {brand['name']} ({brand['slug']})")

    # 5. Получаем все товары
    print("\n📱 Получение товаров:")
    response = requests.get(f"{BASE_URL}/api/v1/products")
    print(f"Status: {response.status_code}")
    products = response.json()
    print(f"Найдено товаров: {len(products)}")
    for product in products:
        print(f"  - {product['title']} (${product['base_price']})")

    # 6. Создаем новую категорию через API
    print("\n➕ Создание новой категории через API:")
    new_category = {"name": "Планшеты", "description": "Категория планшетов"}
    response = requests.post(f"{BASE_URL}/api/v1/categories", json=new_category)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        created_category = response.json()
        print(
            f"✅ Создана категория: {created_category['name']} (ID: {created_category['id']})"
        )

        # 7. Создаем новый товар
        print("\n➕ Создание нового товара через API:")
        new_product = {
            "title": "iPad Pro 12.9",
            "description": "Профессиональный планшет Apple",
            "sku": "IPAD-PRO-001",
            "base_price": 1099.99,
            "old_price": 1199.99,
            "total_stock": 5,
            "category_id": created_category["id"],
            "brand_id": brands[0]["id"] if brands else None,
            "is_featured": True,
        }
        response = requests.post(f"{BASE_URL}/api/v1/products", json=new_product)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            created_product = response.json()
            print(
                f"✅ Создан товар: {created_product['title']} (SKU: {created_product['sku']})"
            )

    # 8. Тестируем поиск
    print("\n🔍 Тестирование поиска:")
    response = requests.get(f"{BASE_URL}/api/v1/products/search?q=Samsung")
    print(f"Status: {response.status_code}")
    search_results = response.json()
    print(f"Найдено по запросу 'Samsung': {len(search_results)} товаров")

    # 9. Тестируем фильтрацию
    print("\n🔽 Тестирование фильтрации (рекомендуемые товары):")
    response = requests.get(f"{BASE_URL}/api/v1/products/featured")
    print(f"Status: {response.status_code}")
    featured_products = response.json()
    print(f"Рекомендуемых товаров: {len(featured_products)}")

    # 10. Получаем информацию об API
    print("\n📋 Информация об API:")
    response = requests.get(f"{BASE_URL}/api/v1")
    print(f"Status: {response.status_code}")
    api_info = response.json()
    print(f"API Name: {api_info['name']}")
    print(f"Version: {api_info['version']}")
    print("Доступные эндпоинты:")
    for endpoint, url in api_info["endpoints"].items():
        print(f"  - {endpoint}: {url}")

    print("\n✅ Все тесты API завершены!")
    print(f"\n🌐 Откройте документацию: {BASE_URL}/docs")
    print(f"📚 Альтернативная документация: {BASE_URL}/redoc")


if __name__ == "__main__":
    test_api()
