from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat import chat_service
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()

@router.post("", response_model=dict)
async def chat(chat_data: dict, db: Session = Depends(get_db)):
    """发送聊天消息（非流式）"""
    try:
        query = chat_data.get("query")
        kb_id = chat_data.get("knowledge_base_id")
        if not query:
            return {"message": "请输入问题", "sources": []}
        
        response = await chat_service.chat(query, kb_id)
        return response
    except Exception as e:
        return {
            "message": f"处理您的请求时出现错误: {str(e)}",
            "sources": []
        }

@router.post("/stream")
async def stream_chat(chat_data: dict, db: Session = Depends(get_db)):
    """流式聊天"""
    async def generate():
        try:
            query = chat_data.get("query")
            kb_id = chat_data.get("knowledge_base_id")
            if not query:
                yield "data: 请输入问题\n\n"
                yield "data: [DONE]\n\n"
                return
            
            async for chunk in chat_service.stream_chat(query, kb_id):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: 处理您的请求时出现错误: {str(e)}\n\n"
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
