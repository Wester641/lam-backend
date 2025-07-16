import sys
import os

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import engine, SessionLocal
from sqlalchemy import text

def test_connection():
    try:
        # Тест подключения
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Подключение к БД успешно!")
            
        # Тест сессии
        db = SessionLocal()
        result = db.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"✅ PostgreSQL версия: {version}")
        db.close()
        
        # Проверка таблиц
        db = SessionLocal()
        result = db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename"))
        tables = [row[0] for row in result.fetchall()]
        print(f"✅ Созданные таблицы ({len(tables)}): {tables}")
        db.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()