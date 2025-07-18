# API Мануал для фронтендщика

Документация по интеграции с E-commerce Backend API.

## 📋 Содержание

- [Базовая информация](#-базовая-информация)
- [Структура данных](#-структура-данных)
- [Основные эндпоинты](#-основные-эндпоинты)
- [Примеры запросов](#-примеры-запросов)
- [JavaScript клиент](#-javascript-клиент)
- [Обработка ошибок](#-обработка-ошибок)

## 🌐 Базовая информация

**Base URL:** `http://localhost:8000/api/v1`

**Content-Type:** `application/json`

**CORS:** Настроен для `localhost:3000`, `localhost:5173`, `localhost:3001`

## 📊 Структура данных

### Товар (Product)

```json
{
  "id": 1,
  "title": "Macbook Air 13 256 M2 Midnight 5",
  "description": "Force Touch trackpad for precise cursor control...",
  "sku": "MBA-256",
  "base_price": 765.0,
  "old_price": 785.0,
  "stock_state": "Available",
  "total_stock": 53,
  "is_featured": true,
  "is_active": true,
  "category_id": 1,
  "brand_id": 1,
  "shop_id": 1,
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00",
  "category": {
    "id": 1,
    "name": "Ноутбуки",
    "slug": "noutbuki"
  },
  "brand": {
    "id": 1,
    "name": "Apple",
    "slug": "apple"
  },
  "shop": {
    "id": 1,
    "name": "L&M Zone",
    "slug": "lm-zone"
  },
  "tags": [
    {
      "id": 1,
      "name": "Macbook",
      "slug": "macbook"
    }
  ],
  "images": [
    {
      "id": 1,
      "url": "https://res.cloudinary.com/dx2cycu19/image/upload/v1747591248/air1_jgyucc.jpg",
      "alt_text": "MacBook Air",
      "is_primary": true,
      "sort_order": 1
    }
  ],
  "variants": [
    {
      "id": 1,
      "attribute_id": 1,
      "price_modifier": 0.0,
      "stock_quantity": 10,
      "attribute": {
        "id": 1,
        "value": "Midnight",
        "attribute_type": {
          "id": 1,
          "name": "Color"
        }
      }
    }
  ]
}
```

### Категория (Category)

```json
{
  "id": 1,
  "name": "Ноутбуки",
  "slug": "noutbuki",
  "description": "Категория ноутбуков",
  "parent_id": null,
  "is_active": true,
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00",
  "children": []
}
```

### Бренд (Brand)

```json
{
  "id": 1,
  "name": "Apple",
  "slug": "apple",
  "logo_url": "https://example.com/apple-logo.png",
  "description": "Американская технологическая компания",
  "is_active": true,
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

## 🔗 Основные эндпоинты

### Товары

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/products` | Список товаров с фильтрацией |
| `GET` | `/products/{id}` | Товар по ID (полная информация) |
| `GET` | `/products/slug/{slug}` | Товар по slug |
| `GET` | `/products/sku/{sku}` | Товар по SKU |
| `GET` | `/products/featured` | Рекомендуемые товары |
| `GET` | `/products/search` | Поиск товаров |
| `POST` | `/products` | Создать товар |
| `PUT` | `/products/{id}` | Обновить товар |
| `DELETE` | `/products/{id}` | Удалить товар |

### Категории

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/categories` | Список категорий |
| `GET` | `/categories/{id}` | Категория по ID |
| `GET` | `/categories/slug/{slug}` | Категория по slug |
| `GET` | `/categories/roots` | Корневые категории |
| `GET` | `/categories/tree` | Дерево категорий |
| `GET` | `/categories/{id}/children` | Дочерние категории |
| `POST` | `/categories` | Создать категорию |
| `PUT` | `/categories/{id}` | Обновить категорию |
| `DELETE` | `/categories/{id}` | Удалить категорию |

### Бренды

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/brands` | Список брендов |
| `GET` | `/brands/{id}` | Бренд по ID |
| `GET` | `/brands/slug/{slug}` | Бренд по slug |
| `GET` | `/brands/popular` | Популярные бренды |
| `POST` | `/brands` | Создать бренд |
| `PUT` | `/brands/{id}` | Обновить бренд |
| `DELETE` | `/brands/{id}` | Удалить бренд |

## 📝 Примеры запросов

### Получить все товары

```javascript
fetch('http://localhost:8000/api/v1/products')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Фильтрация товаров

```javascript
const params = new URLSearchParams({
  category_id: 1,
  brand_id: 2,
  min_price: 100,
  max_price: 1000,
  in_stock: true,
  featured: true,
  sort_by: 'price',
  sort_order: 'desc',
  skip: 0,
  limit: 10
});

fetch(`http://localhost:8000/api/v1/products?${params}`)
  .then(response => response.json())
  .then(data => console.log(data));
```

### Поиск товаров

```javascript
const searchQuery = 'iPhone';
fetch(`http://localhost:8000/api/v1/products/search?q=${searchQuery}&limit=20`)
  .then(response => response.json())
  .then(data => console.log(data));
```

### Получить товар по ID

```javascript
fetch('http://localhost:8000/api/v1/products/1')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Получить рекомендуемые товары

```javascript
fetch('http://localhost:8000/api/v1/products/featured?limit=10')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Получить дерево категорий

```javascript
fetch('http://localhost:8000/api/v1/categories/tree')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Получить популярные бренды

```javascript
fetch('http://localhost:8000/api/v1/brands/popular?limit=10')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Создать товар

```javascript
const productData = {
  title: "iPhone 15 Pro",
  description: "Новый iPhone с чипом A17 Pro",
  sku: "IP15-PRO-001",
  base_price: 999.99,
  old_price: 1099.99,
  total_stock: 50,
  stock_state: "Available",
  category_id: 2,
  brand_id: 1,
  is_featured: true,
  tag_ids: [1, 2, 3],
  image_ids: [1, 2]
};

fetch('http://localhost:8000/api/v1/products', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(productData)
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🛠️ JavaScript клиент

Готовый клиент для работы с API:

```javascript
class EcommerceAPI {
  constructor(baseURL = 'http://localhost:8000/api/v1') {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Товары
  async getProducts(params = {}) {
    const queryParams = new URLSearchParams(params);
    return this.request(`/products?${queryParams}`);
  }

  async getProduct(id) {
    return this.request(`/products/${id}`);
  }

  async getFeaturedProducts(limit = 10) {
    return this.request(`/products/featured?limit=${limit}`);
  }

  async searchProducts(query, params = {}) {
    const queryParams = new URLSearchParams({ q: query, ...params });
    return this.request(`/products/search?${queryParams}`);
  }

  async createProduct(productData) {
    return this.request('/products', {
      method: 'POST',
      body: JSON.stringify(productData)
    });
  }

  // Категории
  async getCategories() {
    return this.request('/categories');
  }

  async getCategoryTree() {
    return this.request('/categories/tree');
  }

  async getCategory(id) {
    return this.request(`/categories/${id}`);
  }

  // Бренды
  async getBrands() {
    return this.request('/brands');
  }

  async getPopularBrands(limit = 10) {
    return this.request(`/brands/popular?limit=${limit}`);
  }

  async getBrand(id) {
    return this.request(`/brands/${id}`);
  }
}

// Использование
const api = new EcommerceAPI();

// Получить все товары
const products = await api.getProducts();

// Поиск товаров
const searchResults = await api.searchProducts('MacBook');

// Фильтрация
const filteredProducts = await api.getProducts({
  category_id: 1,
  min_price: 500,
  max_price: 2000,
  in_stock: true
});
```

## ⚠️ Обработка ошибок

API возвращает стандартные HTTP коды ошибок:

- `200` - Успешно
- `201` - Создано
- `400` - Неверный запрос
- `404` - Не найдено
- `422` - Ошибка валидации
- `500` - Внутренняя ошибка сервера

Пример обработки ошибок:

```javascript
async function handleAPIRequest() {
  try {
    const response = await fetch('http://localhost:8000/api/v1/products/999');
    
    if (!response.ok) {
      if (response.status === 404) {
        console.log('Товар не найден');
        return null;
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Ошибка API:', error.message);
    throw error;
  }
}
```

## 🔍 Параметры фильтрации товаров

| Параметр | Тип | Описание |
|----------|-----|----------|
| `category_id` | number | ID категории |
| `brand_id` | number | ID бренда |
| `min_price` | number | Минимальная цена |
| `max_price` | number | Максимальная цена |
| `in_stock` | boolean | Только в наличии |
| `featured` | boolean | Только рекомендуемые |
| `search` | string | Поиск по названию |
| `sort_by` | string | Поле сортировки (`price`, `created_at`, `title`) |
| `sort_order` | string | Порядок сортировки (`asc`, `desc`) |
| `skip` | number | Пропустить записей (пагинация) |
| `limit` | number | Количество записей (макс. 100) |

## 📱 Адаптация под ваши мок данные

Если нужно адаптировать API под существующую структуру фронтенда, можно создать адаптер:

```javascript
function adaptProductData(apiProduct) {
  return {
    id: apiProduct.id,
    stock_state: apiProduct.stock_state,
    total_stock: apiProduct.total_stock,
    rating: "0.0", // Заглушка, пока нет отзывов
    reviewCount: "0", // Заглушка
    title: apiProduct.title,
    shop_name: apiProduct.shop?.name || "L&M Zone",
    price: apiProduct.base_price,
    old_price: apiProduct.old_price ? `$${apiProduct.old_price}` : "",
    new_price: `$${apiProduct.base_price}`,
    image: apiProduct.images?.find(img => img.is_primary)?.url || "",
    delivered_by: "Aug 02", // Заглушка
    discount: calculateDiscount(apiProduct.old_price, apiProduct.base_price),
    sku: apiProduct.sku,
    description: apiProduct.description || "",
    specifications: {
      spec_images: apiProduct.images?.map(img => img.url) || []
    },
    colors: getProductColors(apiProduct.variants),
    tags: apiProduct.tags?.map(tag => tag.name) || []
  };
}

function calculateDiscount(oldPrice, newPrice) {
  if (oldPrice && oldPrice > newPrice) {
    const percent = Math.round(((oldPrice - newPrice) / oldPrice) * 100);
    return `${percent}%OFF`;
  }
  return "";
}

function getProductColors(variants) {
  return variants
    ?.filter(v => v.attribute?.attribute_type?.name === 'Color')
    .map(v => v.attribute.value) || ["Default"];
}
```

## 🚀 Готово!

Теперь у вас есть полная документация для интеграции фронтенда с API. 

**Полезные ссылки:**
- Swagger документация: http://localhost:8000/docs
- ReDoc документация: http://localhost:8000