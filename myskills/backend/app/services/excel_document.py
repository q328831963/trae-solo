"""Excel文档服务"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.excel_document import ExcelDocument
from app.models.vector import Vector
from app.utils.file_parser import parse_excel
from app.services.embedding import embedding_service
from app.services.vector_utils import vector_utils
from app.services.knowledge_base import knowledge_base_service
from loguru import logger
import os
import uuid
import pandas as pd


class ExcelDocumentService:
    def upload_excel_document(self, db: Session, kb_id: str, file_path: str, file_name: str, file_size: int) -> ExcelDocument:
        """上传Excel文档"""
        try:
            # 解析Excel文件
            sheets = parse_excel(file_path)
            sheet_count = len(sheets)
            
            new_doc = ExcelDocument(
                id=str(uuid.uuid4()),
                knowledge_base_id=kb_id,
                name=file_name,
                file_path=file_path,
                size=file_size,
                sheet_count=sheet_count
            )
            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)
            
            logger.info(f"上传Excel文档成功: {new_doc.name} - {sheet_count}个Sheet")
            return new_doc
        except Exception as e:
            logger.error(f"上传Excel文档失败: {str(e)}")
            db.rollback()
            # 清理上传的文件
            if os.path.exists(file_path):
                os.remove(file_path)
            raise
    
    def chunk_and_store_excel(self, db: Session, doc_id: str, chunk_mode: str = "row_level", include_header: bool = True) -> ExcelDocument:
        """分块并存储Excel文档"""
        doc = self.get_excel_document(db, doc_id)
        if not doc:
            raise ValueError("Excel文档不存在")
        
        try:
            # 解析Excel文件
            sheets = parse_excel(doc.file_path)
            
            # 分块处理
            chunks = []
            if chunk_mode == "row_level":
                chunks = self._row_level_chunking(sheets, include_header)
            elif chunk_mode == "topic_semantic":
                chunks = self._topic_semantic_chunking(sheets, include_header)
            
            doc.chunk_mode = chunk_mode
            doc.chunk_count = len(chunks)
            
            # 生成向量
            vectors = []
            vector_ids = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                # 生成向量
                embedding = embedding_service.get_embedding(chunk["content"])
                
                # 创建向量记录
                vector_id = str(uuid.uuid4())
                vector = Vector(
                    id=vector_id,
                    knowledge_base_id=doc.knowledge_base_id,
                    document_id=doc.id,
                    chunk_id=str(i),
                    content=chunk["content"],
                    embedding=embedding,
                    embedding_dimension=len(embedding),
                    metadata={
                        "document_name": doc.name,
                        "sheet_name": chunk["sheet_name"],
                        "chunk_index": i
                    }
                )
                db.add(vector)
                vectors.append(embedding)
                vector_ids.append(vector_id)
                metadatas.append({
                    "knowledge_base_id": doc.knowledge_base_id,
                    "document_id": doc.id,
                    "document_name": doc.name,
                    "sheet_name": chunk["sheet_name"],
                    "chunk_index": i
                })
            
            # 添加向量到ChromaDB
            if vectors:
                vector_utils.add_vectors(vectors, vector_ids, metadatas)
                doc.vector_count = len(vectors)
            
            db.commit()
            
            # 更新知识库统计信息
            knowledge_base_service.update_knowledge_base_stats(db, doc.knowledge_base_id)
            
            logger.info(f"分块并存储Excel文档成功: {doc.name} - {len(chunks)}分块, {len(vectors)}向量")
            return doc
        except Exception as e:
            logger.error(f"分块并存储Excel文档失败: {str(e)}")
            db.rollback()
            raise
    
    def _row_level_chunking(self, sheets: dict, include_header: bool) -> List[dict]:
        """行级分块"""
        chunks = []
        for sheet_name, data in sheets.items():
            if not data:
                continue
            
            header = data[0] if include_header else None
            for i, row in enumerate(data[1:] if include_header else data):
                if any(cell is not None for cell in row):
                    if header:
                        # 结合表头和行数据
                        row_data = {header[j]: row[j] for j in range(min(len(header), len(row)))}
                        content = "\n".join([f"{k}: {v}" for k, v in row_data.items() if v is not None])
                    else:
                        content = "\n".join([str(cell) for cell in row if cell is not None])
                    
                    if content.strip():
                        chunks.append({
                            "sheet_name": sheet_name,
                            "content": content
                        })
        return chunks
    
    def _topic_semantic_chunking(self, sheets: dict, include_header: bool) -> List[dict]:
        """主题语义分块"""
        chunks = []
        for sheet_name, data in sheets.items():
            if not data:
                continue
            
            header = data[0] if include_header else None
            current_topic = []
            
            for i, row in enumerate(data[1:] if include_header else data):
                if any(cell is not None for cell in row):
                    if header:
                        row_data = {header[j]: row[j] for j in range(min(len(header), len(row)))}
                        content = "\n".join([f"{k}: {v}" for k, v in row_data.items() if v is not None])
                    else:
                        content = "\n".join([str(cell) for cell in row if cell is not None])
                    
                    if content.strip():
                        current_topic.append(content)
                else:
                    # 空行作为主题分隔
                    if current_topic:
                        chunks.append({
                            "sheet_name": sheet_name,
                            "content": "\n\n".join(current_topic)
                        })
                        current_topic = []
            
            # 处理最后一个主题
            if current_topic:
                chunks.append({
                    "sheet_name": sheet_name,
                    "content": "\n\n".join(current_topic)
                })
        return chunks
    
    def get_excel_document(self, db: Session, doc_id: str) -> Optional[ExcelDocument]:
        """获取Excel文档"""
        return db.query(ExcelDocument).filter(ExcelDocument.id == doc_id).first()
    
    def get_excel_documents(self, db: Session, kb_id: str) -> List[ExcelDocument]:
        """获取知识库的所有Excel文档"""
        return db.query(ExcelDocument).filter(ExcelDocument.knowledge_base_id == kb_id).all()
    
    def delete_excel_document(self, db: Session, doc_id: str) -> bool:
        """删除Excel文档"""
        doc = self.get_excel_document(db, doc_id)
        if not doc:
            raise ValueError("Excel文档不存在")
        
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
            
            logger.info(f"删除Excel文档成功: {doc.name}")
            return True
        except Exception as e:
            logger.error(f"删除Excel文档失败: {str(e)}")
            db.rollback()
            raise


excel_document_service = ExcelDocumentService()
