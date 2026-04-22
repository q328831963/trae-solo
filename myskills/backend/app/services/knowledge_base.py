"""知识库服务"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.knowledge_base import KnowledgeBase
from app.models.document import Document
from app.models.vector import Vector
from loguru import logger
import uuid


class KnowledgeBaseService:
    def create_knowledge_base(self, db: Session, name: str, description: str) -> KnowledgeBase:
        """创建知识库"""
        try:
            new_kb = KnowledgeBase(
                id=str(uuid.uuid4()),
                name=name,
                description=description
            )
            db.add(new_kb)
            db.commit()
            db.refresh(new_kb)
            logger.info(f"创建知识库成功: {new_kb.name}")
            return new_kb
        except Exception as e:
            logger.error(f"创建知识库失败: {str(e)}")
            db.rollback()
            raise
    
    def get_knowledge_base(self, db: Session, kb_id: str) -> Optional[KnowledgeBase]:
        """获取知识库"""
        return db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    
    def get_knowledge_bases(self, db: Session) -> List[KnowledgeBase]:
        """获取所有知识库"""
        return db.query(KnowledgeBase).all()
    
    def update_knowledge_base(self, db: Session, kb_id: str, name: Optional[str] = None, description: Optional[str] = None) -> KnowledgeBase:
        """更新知识库"""
        kb = self.get_knowledge_base(db, kb_id)
        if not kb:
            raise ValueError("知识库不存在")
        
        if name:
            kb.name = name
        if description:
            kb.description = description
        
        db.commit()
        db.refresh(kb)
        logger.info(f"更新知识库成功: {kb.name}")
        return kb
    
    def delete_knowledge_base(self, db: Session, kb_id: str) -> bool:
        """删除知识库"""
        kb = self.get_knowledge_base(db, kb_id)
        if not kb:
            raise ValueError("知识库不存在")
        
        try:
            # 删除相关的向量
            vectors = db.query(Vector).filter(Vector.knowledge_base_id == kb_id).all()
            for vector in vectors:
                db.delete(vector)
            
            # 删除相关的文档
            documents = db.query(Document).filter(Document.knowledge_base_id == kb_id).all()
            for doc in documents:
                db.delete(doc)
            
            # 删除知识库
            db.delete(kb)
            db.commit()
            logger.info(f"删除知识库成功: {kb.name}")
            return True
        except Exception as e:
            logger.error(f"删除知识库失败: {str(e)}")
            db.rollback()
            raise
    
    def update_knowledge_base_stats(self, db: Session, kb_id: str):
        """更新知识库统计信息"""
        kb = self.get_knowledge_base(db, kb_id)
        if not kb:
            return
        
        # 计算文档数量
        document_count = db.query(Document).filter(Document.knowledge_base_id == kb_id).count()
        
        # 计算向量数量
        vector_count = db.query(Vector).filter(Vector.knowledge_base_id == kb_id).count()
        
        kb.document_count = document_count
        kb.vector_count = vector_count
        
        db.commit()
        logger.info(f"更新知识库统计信息: {kb.name} - {document_count}文档, {vector_count}向量")


knowledge_base_service = KnowledgeBaseService()
