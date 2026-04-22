from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.vector import vector_service
from typing import List

router = APIRouter()

@router.get("/knowledge-bases/{kb_id}/vectors", response_model=List[dict])
async def get_vectors(kb_id: str, db: Session = Depends(get_db)):
    """获取向量列表"""
    try:
        return vector_service.get_vectors(db, kb_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/knowledge-bases/{kb_id}/vectors/rebuild", response_model=dict)
async def rebuild_vectors(kb_id: str, db: Session = Depends(get_db)):
    """重建向量索引"""
    try:
        return vector_service.rebuild_vectors(db, kb_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/retrieve", response_model=List[dict])
async def retrieve_vectors(query_data: dict, db: Session = Depends(get_db)):
    """向量检索"""
    try:
        query = query_data.get("query")
        knowledge_base_id = query_data.get("knowledge_base_id")
        if not query:
            raise ValueError("查询文本不能为空")
        return vector_service.retrieve_vectors(db, query, knowledge_base_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
