from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """应用配置类"""
    # 应用配置
    app_name: str = "MySkills Backend"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = True
    app_version: str = "1.0.0"
    
    # 数据库配置
    database_url: str = "sqlite:///./app.db"
    
    # 向量数据库配置
    chroma_host: str = "chromadb"
    chroma_port: int = 8000
    chroma_collection: str = "myskills_collection"
    
    # 嵌入模型配置
    embedding_model: str = "BAAI/bge-large-zh-v1.5"
    embedding_device: str = "cpu"
    
    # 文件存储
    upload_dir: str = "./uploads"
    max_upload_size: int = 104857600  # 100MB
    
    # CORS配置
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # LLM配置
    llm_api_url: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_model: str = "gpt-4o-mini"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
