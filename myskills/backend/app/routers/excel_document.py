from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.excel_document import excel_document_service
from app.services.knowledge_base import knowledge_base_service
from typing import List
import os
from app.config import settings

router = APIRouter()

@router.get("/knowledge-bases/{kb_id}/excel-documents", response_model=List[dict])
async def get_excel_documents(kb_id: str, db: Session = Depends(get_db)):
    """获取Excel文档列表"""
    try:
        # 验证知识库是否存在
        kb = knowledge_base_service.get_knowledge_base(db, kb_id)
        if not kb:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        documents = excel_document_service.get_excel_documents(db, kb_id)
        return [
            {
                "id": doc.id,
                "name": doc.name,
                "sheet_count": doc.sheet_count,
                "chunk_mode": doc.chunk_mode,
                "chunk_count": doc.chunk_count,
                "vector_count": doc.vector_count,
                "created_at": doc.created_at
            }
            for doc in documents
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/knowledge-bases/{kb_id}/excel-documents/upload", response_model=dict)
async def upload_excel_document(
    kb_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传Excel文档"""
    try:
        # 验证知识库是否存在
        kb = knowledge_base_service.get_knowledge_base(db, kb_id)
        if not kb:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        # 创建上传目录
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(settings.upload_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        new_doc = excel_document_service.upload_excel_document(
            db=db,
            kb_id=kb_id,
            file_path=file_path,
            file_name=file.filename,
            file_size=len(content)
        )
        
        return {
            "id": new_doc.id,
            "name": new_doc.name,
            "size": new_doc.size
        }
    except HTTPException:
        raise
    except Exception as e:
        # 清理上传的文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{doc_id}/chunk-and-store", response_model=dict)
async def chunk_and_store_excel(doc_id: str, chunk_data: dict, db: Session = Depends(get_db)):
    """分块并存储Excel文档"""
    try:
        doc = excel_document_service.chunk_and_store_excel(
            db=db,
            doc_id=doc_id,
            chunk_mode=chunk_data.get("chunk_mode", "row_level"),
            include_header=chunk_data.get("include_header", True)
        )
        return {
            "id": doc.id,
            "chunk_count": doc.chunk_count,
            "vector_count": doc.vector_count
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chunk-preview", response_model=dict)
async def preview_chunk(chunk_data: dict):
    """预览分块效果"""
    # 这里只是一个占位实现，实际预览逻辑需要在服务层实现
    return {
        "chunks": [
            {"id": "1", "content": "第一块内容"},
            {"id": "2", "content": "第二块内容"}
        ]
    }

@router.delete("/{doc_id}", response_model=dict)
async def delete_excel_document(doc_id: str, db: Session = Depends(get_db)):
    """删除Excel文档"""
    try:
        excel_document_service.delete_excel_document(db, doc_id)
        return {"message": "Excel文档删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
