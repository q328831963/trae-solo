from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/select-knowledge-bases", response_model=dict)
async def select_knowledge_bases(query_data: dict, db: Session = Depends(get_db)):
    """选择知识库（智能体推荐）"""
    # 这里只是一个占位实现，实际推荐逻辑需要在服务层实现
    return {
        "recommended_knowledge_bases": [
            {
                "id": "1",
                "name": "技术文档",
                "score": 0.95
            },
            {
                "id": "2",
                "name": "产品文档",
                "score": 0.85
            }
        ]
    }
