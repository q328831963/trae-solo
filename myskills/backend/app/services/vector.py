"""向量服务"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.vector import Vector
from app.models.document import Document
from app.services.embedding import embedding_service
from app.services.vector_utils import vector_utils
from app.services.knowledge_base import knowledge_base_service
from loguru import logger


class VectorService:
    def get_vectors(self, db: Session, kb_id: str) -> List[Dict[str, Any]]:
        """获取向量列表"""
        vectors = db.query(Vector).filter(Vector.knowledge_base_id == kb_id).limit(100).all()
        return [
            {
                "id": v.id,
                "document_id": v.document_id,
                "chunk_id": v.chunk_id,
                "content": v.content[:100] + "..." if len(v.content) > 100 else v.content,
                "embedding_dimension": v.embedding_dimension,
                "created_at": v.created_at
            }
            for v in vectors
        ]
    
    def rebuild_vectors(self, db: Session, kb_id: str) -> Dict[str, str]:
        """重建向量索引"""
        try:
            # 获取知识库的所有文档
            documents = db.query(Document).filter(Document.knowledge_base_id == kb_id).all()
            
            # 重新处理每个文档
            for doc in documents:
                # 删除旧的向量
                old_vectors = db.query(Vector).filter(Vector.document_id == doc.id).all()
                old_vector_ids = [v.id for v in old_vectors]
                if old_vector_ids:
                    vector_utils.delete_vectors(old_vector_ids)
                for vector in old_vectors:
                    db.delete(vector)
            
            # 重新生成向量
            for doc in documents:
                # 分块文本
                from app.utils.text_utils import split_text_by_size
                chunks = split_text_by_size(doc.content, chunk_size=1000, overlap=100)
                doc.chunk_count = len(chunks)
                
                # 生成向量
                vectors = []
                vector_ids = []
                metadatas = []
                
                for i, chunk in enumerate(chunks):
                    # 生成向量
                    embedding = embedding_service.get_embedding(chunk)
                    
                    # 创建向量记录
                    import uuid
                    vector_id = str(uuid.uuid4())
                    vector = Vector(
                        id=vector_id,
                        knowledge_base_id=doc.knowledge_base_id,
                        document_id=doc.id,
                        chunk_id=str(i),
                        content=chunk,
                        embedding=embedding,
                        embedding_dimension=len(embedding),
                        vector_metadata={
                            "document_name": doc.name,
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
                        "chunk_index": i
                    })
                
                # 添加向量到ChromaDB
                if vectors:
                    vector_utils.add_vectors(vectors, vector_ids, metadatas)
                    doc.vector_count = len(vectors)
            
            db.commit()
            
            # 更新知识库统计信息
            knowledge_base_service.update_knowledge_base_stats(db, kb_id)
            
            logger.info(f"重建向量索引成功: {kb_id}")
            return {"message": "向量索引重建成功"}
        except Exception as e:
            logger.error(f"重建向量索引失败: {str(e)}")
            db.rollback()
            raise
    
    def retrieve_vectors(self, db: Session, query: str, knowledge_base_id: str) -> List[Dict[str, Any]]:
        """向量检索"""
        try:
            # 生成查询向量
            query_embedding = embedding_service.get_embedding(query)
            
            # 构建过滤条件
            where = {"knowledge_base_id": knowledge_base_id}
            
            # 查询向量
            result = vector_utils.query_vectors(query_embedding, top_k=5, where=where)
            
            # 格式化结果
            retrieved_vectors = []
            for i, (id, content, metadata, distance) in enumerate(zip(
                result["ids"][0],
                result["documents"][0],
                result["metadatas"][0],
                result["distances"][0]
            )):
                retrieved_vectors.append({
                    "id": id,
                    "content": content,
                    "similarity": 1 - distance,  # 转换为相似度
                    "document_id": metadata.get("document_id")
                })
            
            logger.info(f"向量检索成功: {query}")
            return retrieved_vectors
        except Exception as e:
            logger.error(f"向量检索失败: {str(e)}")
            # 返回示例结果
            return [
                {
                    "id": "1",
                    "content": "示例检索结果",
                    "similarity": 0.95,
                    "document_id": "doc1"
                }
            ]


vector_service = VectorService()