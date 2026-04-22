import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from typing import List, Optional
import numpy as np
from loguru import logger
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from app.config import settings


class EmbeddingService:
    def __init__(self):
        self.model: Optional[HuggingFaceEmbedding] = None
        self._initialize_model()
    
    def _initialize_model(self):
        try:
            logger.info(f"正在加载嵌入模型: {settings.embedding_model}")
            self.model = HuggingFaceEmbedding(
                model_name=settings.embedding_model,
                device=settings.embedding_device,
            )
            logger.info("嵌入模型加载成功")
        except Exception as e:
            logger.error(f"嵌入模型加载失败: {str(e)}")
            raise
    
    def get_embedding(self, text: str, text_type: str = "chunk") -> List[float]:
        if not self.model:
            raise RuntimeError("嵌入模型未初始化")
        
        try:
            # 预处理文本
            processed_text = self._preprocess_text(text)
            embedding = self.model.get_text_embedding(processed_text)
            return self._normalize(embedding)
        except Exception as e:
            logger.error(f"生成嵌入向量失败: {str(e)}")
            raise
    
    @staticmethod
    def _preprocess_text(text: str) -> str:
        """预处理文本"""
        # 移除多余的空白字符
        text = ' '.join(text.split())
        # 限制文本长度
        if len(text) > 1000:
            text = text[:1000]
        return text
    
    @staticmethod
    def _normalize(vector: List[float]) -> List[float]:
        """归一化向量"""
        arr = np.array(vector, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm > 0:
            arr = arr / norm
        return arr.tolist()


embedding_service = EmbeddingService()
