from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.knowledge_base import knowledge_base_service
from typing import List

router = APIRouter()

@router.get("", response_model=List[dict])
async def get_knowledge_bases(db: Session = Depends(get_db)):
    """获取知识库列表"""
    knowledge_bases = knowledge_base_service.get_knowledge_bases(db)
    return [
        {
            "id": kb.id,
            "name": kb.name,
            "description": kb.description,
            "document_count": kb.document_count,
            "vector_count": kb.vector_count,
            "created_at": kb.created_at
        }
        for kb in knowledge_bases
    ]

@router.post("", response_model=dict)
async def create_knowledge_base(kb_data: dict, db: Session = Depends(get_db)):
    """创建知识库"""
    try:
        new_kb = knowledge_base_service.create_knowledge_base(
            db=db,
            name=kb_data.get("name"),
            description=kb_data.get("description")
        )
        return {
            "id": new_kb.id,
            "name": new_kb.name,
            "description": new_kb.description
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{kb_id}", response_model=dict)
async def get_knowledge_base(kb_id: str, db: Session = Depends(get_db)):
    """获取知识库详情"""
    kb = knowledge_base_service.get_knowledge_base(db, kb_id)
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")
    return {
        "id": kb.id,
        "name": kb.name,
        "description": kb.description,
        "document_count": kb.document_count,
        "vector_count": kb.vector_count,
        "summary": kb.summary,
        "created_at": kb.created_at
    }

@router.put("/{kb_id}", response_model=dict)
async def update_knowledge_base(kb_id: str, kb_data: dict, db: Session = Depends(get_db)):
    """更新知识库"""
    try:
        kb = knowledge_base_service.update_knowledge_base(
            db=db,
            kb_id=kb_id,
            name=kb_data.get("name"),
            description=kb_data.get("description")
        )
        return {
            "id": kb.id,
            "name": kb.name,
            "description": kb.description
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{kb_id}", response_model=dict)
async def delete_knowledge_base(kb_id: str, db: Session = Depends(get_db)):
    """删除知识库"""
    try:
        knowledge_base_service.delete_knowledge_base(db, kb_id)
        return {"message": "知识库删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{kb_id}/generate-summary", response_model=dict)
async def generate_summary(kb_id: str, db: Session = Depends(get_db)):
    """生成知识库摘要"""
    try:
        # 这里只是一个占位实现，实际摘要生成逻辑需要在服务层实现
        return {"message": "摘要生成任务已启动"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
