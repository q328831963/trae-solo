from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import uuid


class ExcelDocument(Base):
    """Excel文档模型"""
    __tablename__ = "excel_documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    knowledge_base_id = Column(String, ForeignKey("knowledge_bases.id"), nullable=False)
    name = Column(String(255), nullable=False)
    file_path = Column(Text)
    size = Column(Integer)
    sheet_count = Column(Integer, default=0)
    chunk_mode = Column(String(50), default="row_level")  # row_level, topic_semantic
    chunk_count = Column(Integer, default=0)
    vector_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
