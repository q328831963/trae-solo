from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.agent_template import AgentTemplate
from typing import List

router = APIRouter()

@router.get("", response_model=List[dict])
async def get_agent_templates(db: Session = Depends(get_db)):
    """获取智能体模板列表"""
    templates = db.query(AgentTemplate).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "type": t.type,
            "description": t.description,
            "status": t.status
        }
        for t in templates
    ]

@router.get("/{agent_id}", response_model=dict)
async def get_agent_template(agent_id: str, db: Session = Depends(get_db)):
    """获取智能体模板详情"""
    template = db.query(AgentTemplate).filter(AgentTemplate.id == agent_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="智能体模板不存在")
    return {
        "id": template.id,
        "name": template.name,
        "type": template.type,
        "description": template.description,
        "status": template.status,
        "templates": template.templates
    }
