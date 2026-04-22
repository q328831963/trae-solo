from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base
import uuid


class AgentTemplate(Base):
    """智能体模板模型"""
    __tablename__ = "agent_templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # selector, assistant, analyzer
    description = Column(Text)
    status = Column(String(50), default="active")  # active, inactive
    templates = Column(JSON, nullable=False)  # 模板列表（JSON数组）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
