from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    knowledge_base, document, vector, excel_document,
    skill, chat, agent, agent_template, system
)
from app.config import settings
from app.database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(knowledge_base.router, prefix="/api/knowledge-bases", tags=["knowledge-bases"])
app.include_router(document.router, prefix="/api/documents", tags=["documents"])
app.include_router(vector.router, prefix="/api/vectors", tags=["vectors"])
app.include_router(excel_document.router, prefix="/api/excel-documents", tags=["excel-documents"])
app.include_router(skill.router, prefix="/api/skill", tags=["skill"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
app.include_router(agent_template.router, prefix="/api/agent-templates", tags=["agent-templates"])
app.include_router(system.router, prefix="/api/system", tags=["system"])

@app.get("/")
async def root():
    return {"message": "MySkills API", "version": settings.app_version}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
