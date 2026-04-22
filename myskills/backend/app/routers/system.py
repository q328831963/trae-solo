from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings

router = APIRouter()

@router.get("/health", response_model=dict)
async def health_check(db: Session = Depends(get_db)):
    """系统健康检查"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env
    }

@router.get("/info", response_model=dict)
async def system_info(db: Session = Depends(get_db)):
    """系统信息"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "database": settings.database_url,
        "embedding_model": settings.embedding_model
    }
