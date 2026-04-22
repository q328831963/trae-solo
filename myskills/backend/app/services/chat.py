"""聊天服务"""

from typing import List, Dict, Any, AsyncGenerator
import httpx
from app.config import settings
from app.services.embedding import embedding_service
from app.services.vector_utils import vector_utils
from loguru import logger


class ChatService:
    async def chat(self, query: str, kb_id: str = None) -> Dict[str, Any]:
        """非流式聊天"""
        try:
            # 生成查询向量
            query_embedding = embedding_service.get_embedding(query)
            
            # 构建查询条件
            where = None
            if kb_id:
                where = {"knowledge_base_id": kb_id}
            
            # 检索相关向量
            result = vector_utils.query_vectors(
                query_vector=query_embedding,
                top_k=5,
                where=where
            )
            
            # 构建上下文
            context = "\n\n".join([c for c in result.get("documents", [[]])[0] if c])
            
            # 构建提示词
            prompt = f"基于以下上下文回答问题：\n\n{context}\n\n问题：{query}\n回答："
            
            # 调用LLM API
            response = await self._call_llm(prompt)
            
            # 提取来源
            sources = []
            metadatas = result.get("metadatas", [[]])[0]
            for metadata in metadatas:
                if metadata and "document_name" in metadata:
                    sources.append({
                        "id": metadata.get("document_id", ""),
                        "name": metadata.get("document_name", "")
                    })
            
            return {
                "message": response,
                "sources": sources
            }
        except Exception as e:
            logger.error(f"聊天失败: {str(e)}")
            return {
                "message": "抱歉，处理您的请求时出现错误，请重试。",
                "sources": []
            }
    
    async def stream_chat(self, query: str, kb_id: str = None) -> AsyncGenerator[str, None]:
        """流式聊天"""
        try:
            # 生成查询向量
            query_embedding = embedding_service.get_embedding(query)
            
            # 构建查询条件
            where = None
            if kb_id:
                where = {"knowledge_base_id": kb_id}
            
            # 检索相关向量
            result = vector_utils.query_vectors(
                query_vector=query_embedding,
                top_k=5,
                where=where
            )
            
            # 构建上下文
            context = "\n\n".join([c for c in result.get("documents", [[]])[0] if c])
            
            # 构建提示词
            prompt = f"基于以下上下文回答问题：\n\n{context}\n\n问题：{query}\n回答："
            
            # 流式调用LLM API
            async for chunk in self._stream_llm(prompt):
                yield chunk
        except Exception as e:
            logger.error(f"流式聊天失败: {str(e)}")
            yield "抱歉，处理您的请求时出现错误，请重试。"
    
    async def _call_llm(self, prompt: str) -> str:
        """调用LLM API"""
        if not settings.llm_api_url or not settings.llm_api_key:
            return "LLM API未配置，无法生成回答。"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.llm_api_url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {settings.llm_api_key}"
                    },
                    json={
                        "model": settings.llm_model,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
                )
                
                response.raise_for_status()
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"调用LLM API失败: {str(e)}")
            return "调用LLM API失败，请检查配置。"
    
    async def _stream_llm(self, prompt: str) -> AsyncGenerator[str, None]:
        """流式调用LLM API"""
        if not settings.llm_api_url or not settings.llm_api_key:
            yield "LLM API未配置，无法生成回答。"
            return
        
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    settings.llm_api_url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {settings.llm_api_key}"
                    },
                    json={
                        "model": settings.llm_model,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1000,
                        "stream": True
                    }
                ) as response:
                    response.raise_for_status()
                    
                    async for chunk in response.aiter_bytes():
                        if chunk:
                            try:
                                # 解析SSE格式
                                chunk_str = chunk.decode('utf-8')
                                lines = chunk_str.split('\n')
                                for line in lines:
                                    if line.startswith('data: '):
                                        data = line[6:]
                                        if data != '[DONE]':
                                            import json
                                            data_json = json.loads(data)
                                            content = data_json.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                            if content:
                                                yield content
                            except Exception as e:
                                logger.error(f"解析流式响应失败: {str(e)}")
        except Exception as e:
            logger.error(f"流式调用LLM API失败: {str(e)}")
            yield "调用LLM API失败，请检查配置。"


chat_service = ChatService()
