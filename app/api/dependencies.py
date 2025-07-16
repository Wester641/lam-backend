from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal

def get_db() -> Generator:
    """Dependency для получения сессии БД"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user():
    """Dependency для получения текущего пользователя (заглушка)"""
    # TODO: Реализовать аутентификацию
    return {"id": 1, "username": "admin"}

def require_admin(current_user=Depends(get_current_user)):
    """Dependency для проверки прав администратора"""
    # TODO: Реализовать проверку прав
    return current_user