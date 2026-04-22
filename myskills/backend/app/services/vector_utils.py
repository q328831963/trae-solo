"""向量工具函数"""

from typing import List, Dict, Any
import chromadb
from app.config import settings
from loguru import logger


class VectorUtils:
    def __init__(self):
        self.client = None
        self.collection = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化ChromaDB客户端"""
        try:
            logger.info(f"正在连接ChromaDB: {settings.chroma_host}:{settings.chroma_port}")
            self.client = chromadb.HttpClient(
                host=settings.chroma_host,
                port=settings.chroma_port
            )
            # 创建或获取集合
            self.collection = self.client.get_or_create_collection(
                name=settings.chroma_collection
            )
            logger.info("ChromaDB连接成功")
        except Exception as e:
            logger.error(f"ChromaDB连接失败: {str(e)}")
            # 降级为内存模式
            logger.info("降级为内存模式")
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(
                name=settings.chroma_collection
            )
    
    def add_vectors(self, vectors: List[List[float]], ids: List[str], metadatas: List[Dict[str, Any]]):
        """添加向量到数据库"""
        try:
            self.collection.add(
                embeddings=vectors,
                ids=ids,
                metadatas=metadatas
            )
            logger.info(f"成功添加{len(vectors)}个向量")
        except Exception as e:
            logger.error(f"添加向量失败: {str(e)}")
            raise
    
    def query_vectors(self, query_vector: List[float], top_k: int = 5, where: Dict[str, Any] = None):
        """查询向量"""
        try:
            result = self.collection.query(
                query_embeddings=[query_vector],
                n_results=top_k,
                where=where
            )
            return result
        except Exception as e:
            logger.error(f"查询向量失败: {str(e)}")
            raise
    
    def delete_vectors(self, ids: List[str]):
        """删除向量"""
        try:
            self.collection.delete(ids=ids)
            logger.info(f"成功删除{len(ids)}个向量")
        except Exception as e:
            logger.error(f"删除向量失败: {str(e)}")
            raise
    
    def get_vector_count(self):
        """获取向量数量"""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"获取向量数量失败: {str(e)}")
            return 0


vector_utils = VectorUtils()
