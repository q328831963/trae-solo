"""文档服务"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.vector import Vector
from app.utils.file_parser import parse_file
from app.utils.text_utils import split_text_by_size, clean_text
from app.services.embedding import embedding_service
from app.services.vector_utils import vector_utils
from app.services.knowledge_base import knowledge_base_service
from loguru import logger
import os
import uuid


class DocumentService:
    def create_document(self, db: Session, kb_id: str, name: str, document_type: str, content: str) -> Document:
        """创建文档"""
        try:
            new_doc = Document(
                id=str(uuid.uuid4()),
                knowledge_base_id=kb_id,
                name=name,
                document_type=document_type,
                content=content
            )
            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)
            
            # 处理文档分块和向量生成
            self.process_document(db, new_doc)
            
            # 更新知识库统计信息
            knowledge_base_service.update_knowledge_base_stats(db, kb_id)
            
            logger.info(f"创建文档成功: {new_doc.name}")
            return new_doc
        except Exception as e:
            logger.error(f"创建文档失败: {str(e)}")
            db.rollback()
            raise
    
    def upload_document(self, db: Session, kb_id: str, file_path: str, file_name: str, file_size: int) -> Document:
        """上传文档"""
        try:
            # 解析文件
            content = parse_file(file_path)
            content = clean_text(content)
            
            # 确定文档类型
            document_type = file_name.split('.')[-1].lower()
            
            new_doc = Document(
                id=str(uuid.uuid4()),
                knowledge_base_id=kb_id,
                name=file_name,
                document_type=document_type,
                file_path=file_path,
                size=file_size,
                content=content
            )
            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)
            
            # 处理文档分块和向量生成
            self.process_document(db, new_doc)
            
            # 更新知识库统计信息
            knowledge_base_service.update_knowledge_base_stats(db, kb_id)
            
            logger.info(f"上传文档成功: {new_doc.name}")
            return new_doc
        except Exception as e:
            logger.error(f"上传文档失败: {str(e)}")
            db.rollback()
            # 清理上传的文件
            if os.path.exists(file_path):
                os.remove(file_path)
            raise
    
    def process_document(self, db: Session, document: Document):
        """处理文档（分块和向量生成）"""
        try:
            # 分块文本
            chunks = split_text_by_size(document.content, chunk_size=1000, overlap=100)
            document.chunk_count = len(chunks)
            
            # 生成向量
            vectors = []
            vector_ids = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                # 生成向量
                embedding = embedding_service.get_embedding(chunk)
                
                # 创建向量记录
                vector_id = str(uuid.uuid4())
                vector = Vector(
                    id=vector_id,
                    knowledge_base_id=document.knowledge_base_id,
                    document_id=document.id,
                    chunk_id=str(i),
                    content=chunk,
                    embedding=embedding,
                    embedding_dimension=len(embedding),
                    metadata={
                        "document_name": document.name,
                        "chunk_index": i
                    }
                )
                db.add(vector)
                vectors.append(embedding)
                vector_ids.append(vector_id)
                metadatas.append({
                    "knowledge_base_id": document.knowledge_base_id,
                    "document_id": document.id,
                    "document_name": document.name,
                    "chunk_index": i
                })
            
            # 添加向量到ChromaDB
            if vectors:
                vector_utils.add_vectors(vectors, vector_ids, metadatas)
                document.vector_count = len(vectors)
            
            db.commit()
            logger.info(f"处理文档成功: {document.name} - {len(chunks)}分块, {len(vectors)}向量")
        except Exception as e:
            logger.error(f"处理文档失败: {str(e)}")
            db.rollback()
            raise
    
    def get_document(self, db: Session, doc_id: str) -> Optional[Document]:
        """获取文档"""
        return db.query(Document).filter(Document.id == doc_id).first()
    
    def get_documents(self, db: Session, kb_id: str) -> List[Document]:
        """获取知识库的所有文档"""
        return db.query(Document).filter(Document.knowledge_base_id == kb_id).all()
    
    def delete_document(self, db: Session, doc_id: str) -> bool:
        """删除文档"""
        doc = self.get_document(db, doc_id)
        if not doc:
            raise ValueError("文档不存在")
        
        try:
            # 获取知识库ID
            kb_id = doc.knowledge_base_id
            
            # 删除相关的向量
            vectors = db.query(Vector).filter(Vector.document_id == doc_id).all()
            vector_ids = [v.id for v in vectors]
            if vector_ids:
                vector_utils.delete_vectors(vector_ids)
            for vector in vectors:
                db.delete(vector)
            
            # 删除文件
            if doc.file_path and os.path.exists(doc.file_path):
                os.remove(doc.file_path)
            
            # 删除文档
            db.delete(doc)
            db.commit()
            
            # 更新知识库统计信息
            knowledge_base_service.update_knowledge_base_stats(db, kb_id)
            
            logger.info(f"删除文档成功: {doc.name}")
            return True
        except Exception as e:
            logger.error(f"删除文档失败: {str(e)}")
            db.rollback()
            raise


document_service = DocumentService()
