from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Vector(Base):
    """向量模型"""
    __tablename__ = "vectors"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    knowledge_base_id = Column(String, ForeignKey("knowledge_bases.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    chunk_id = Column(String(255))
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=False)  # 向量嵌入（JSON数组）
    embedding_dimension = Column(Integer)
    metadata = Column(JSON)  # 元数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())
