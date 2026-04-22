# MySkills - 私有文档Skill系统

MySkills是一个全栈的私有文档Skill系统，允许用户上传和管理私有文档（支持MD、TXT、PDF、DOCX、Excel格式），通过向量检索技术构建知识库，并提供AI对话功能，使AI能够基于用户的私有文档回答问题。

## 技术栈

### 后端
- **框架**: Python FastAPI
- **向量数据库**: ChromaDB
- **嵌入模型**: BAAI/bge-large-zh-v1.5（通过HuggingFaceEmbedding）
- **ORM**: SQLAlchemy + Alembic（数据库迁移）
- **数据库**: SQLite（默认，可通过配置更改）
- **文件解析**: 支持MD、TXT、PDF、DOCX、Excel（使用python-docx、pdfplumber、openpyxl等）
- **异步处理**: 使用FastAPI的异步支持
- **日志**: loguru
- **环境配置**: Pydantic Settings
- **CORS**: 支持跨域请求
- **API文档**: 自动生成OpenAPI文档（Swagger UI）

### 前端
- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **UI组件库**: shadcn/ui + Tailwind CSS
- **路由**: React Router DOM
- **HTTP客户端**: Axios
- **图标**: Lucide React
- **状态管理**: React Hooks（useState, useEffect）
- **代码质量**: ESLint + Prettier

### 基础设施
- **容器化**: Docker + Docker Compose
- **环境变量**: 使用.env文件管理配置
- **部署**: 支持单机Docker部署

## 核心功能

1. **知识库管理**: 创建、编辑、删除知识库，生成摘要
2. **文档管理**: 上传、创建、查看、删除文档，支持多种格式
3. **Excel文档管理**: 专门处理Excel文件，支持行级和主题语义分块
4. **向量管理**: 测试向量检索，重建向量索引
5. **AI对话**: 基于私有文档的智能对话，支持流式响应
6. **Skill配置**: 配置Function Calling和检索参数
7. **调试面板**: 测试Skill调用效果，查看检索结果
8. **智能体管理**: 管理智能体提示词模板
9. **系统健康监控**: 系统状态检查

## 快速开始

### 使用Docker Compose启动

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd myskills
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑.env文件，配置必要的参数
   ```

3. **启动服务**
   ```bash
   docker-compose up -d
   ```

4. **访问服务**
   - 前端: http://localhost:5173
   - 后端API文档: http://localhost:8000/api/docs
   - 向量数据库: http://localhost:8001

### 开发环境启动

#### 后端启动
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## API端点

### 知识库相关
- `GET /api/knowledge-bases` - 获取知识库列表
- `POST /api/knowledge-bases` - 创建知识库
- `GET /api/knowledge-bases/{kb_id}` - 获取知识库详情
- `PUT /api/knowledge-bases/{kb_id}` - 更新知识库
- `DELETE /api/knowledge-bases/{kb_id}` - 删除知识库
- `POST /api/knowledge-bases/{kb_id}/generate-summary` - 生成知识库摘要

### 文档相关
- `GET /api/knowledge-bases/{kb_id}/documents` - 获取文档列表
- `POST /api/knowledge-bases/{kb_id}/documents` - 创建文档（文本）
- `POST /api/knowledge-bases/{kb_id}/documents/upload` - 上传文档文件
- `GET /api/documents/{doc_id}` - 获取文档详情
- `DELETE /api/documents/{doc_id}` - 删除文档

### Excel文档相关
- `GET /api/knowledge-bases/{kb_id}/excel-documents` - 获取Excel文档列表
- `POST /api/knowledge-bases/{kb_id}/excel-documents/upload` - 上传Excel文档
- `POST /api/excel-documents/{doc_id}/chunk-and-store` - 分块并存储Excel文档
- `POST /api/excel-documents/chunk-preview` - 预览分块效果
- `DELETE /api/excel-documents/{doc_id}` - 删除Excel文档

### 向量相关
- `GET /api/knowledge-bases/{kb_id}/vectors` - 获取向量列表
- `POST /api/knowledge-bases/{kb_id}/vectors/rebuild` - 重建向量索引
- `POST /api/vectors/retrieve` - 向量检索

### 聊天相关
- `POST /api/chat` - 发送聊天消息（非流式）
- `POST /api/chat/stream` - 流式聊天

### Skill相关
- `GET /api/skill/config` - 获取Skill配置
- `PUT /api/skill/config` - 更新Skill配置
- `GET /api/skill/metadata` - 获取Function Calling元数据
- `POST /api/skill/test` - 测试Skill调用

### 智能体相关
- `POST /api/agent/select-knowledge-bases` - 选择知识库（智能体推荐）
- `GET /api/agent-templates` - 获取智能体模板列表
- `GET /api/agent-templates/{agent_id}` - 获取智能体模板详情

### 系统相关
- `GET /api/system/health` - 系统健康检查
- `GET /api/system/info` - 系统信息

## 项目结构

```
myskills/
├── backend/                    # 后端代码
│   ├── app/                    # 应用代码
│   ├── alembic/               # 数据库迁移
│   ├── requirements.txt       # Python依赖
│   ├── Dockerfile             # 后端Docker镜像
│   └── .env.example           # 环境变量示例
├── frontend/                  # 前端代码
│   ├── src/                   # 源码
│   ├── public/               # 静态资源
│   ├── package.json          # 前端依赖
│   ├── Dockerfile            # 前端Docker镜像
│   └── ...
├── docker-compose.yml        # Docker Compose配置
├── .env                      # 环境变量
├── .env.example              # 环境变量示例
└── README.md                 # 项目说明
```

## 配置说明

### 后端配置（.env）
- `DATABASE_URL`: 数据库连接URL
- `CHROMA_HOST`: 向量数据库主机
- `CHROMA_PORT`: 向量数据库端口
- `EMBEDDING_MODEL`: 嵌入模型名称
- `EMBEDDING_DEVICE`: 嵌入模型运行设备（cpu或cuda）
- `UPLOAD_DIR`: 文件上传目录
- `MAX_UPLOAD_SIZE`: 最大上传文件大小
- `CORS_ORIGINS`: 允许的CORS来源
- `LLM_API_URL`: LLM API地址（可选）
- `LLM_API_KEY`: LLM API密钥（可选）
- `LLM_MODEL`: LLM模型名称（可选）

### 前端配置
- `VITE_API_BASE_URL`: API基础URL

## 故障排除

### 常见问题
1. **嵌入模型下载失败**: 检查网络连接，配置HF_ENDPOINT镜像
2. **向量检索效果差**: 调整分块大小、重叠参数，或更换嵌入模型
3. **内存不足**: 减少批量处理大小，使用GPU加速
4. **文件上传失败**: 检查文件大小限制和文件格式支持
5. **数据库连接失败**: 检查数据库URL配置和网络连接

### 日志查看
```bash
# 查看后端日志
docker-compose logs backend

# 查看前端日志
docker-compose logs frontend

# 查看向量数据库日志
docker-compose logs chromadb
```

## 后续开发建议

### 功能增强
1. **多语言支持**: 添加英文界面和文档处理
2. **文档版本控制**: 支持文档版本管理和回滚
3. **协作功能**: 添加团队协作和权限管理
4. **API密钥管理**: 为外部集成提供API密钥管理
5. **插件系统**: 支持自定义文档解析器和向量模型插件

### 性能优化
1. **向量索引优化**: 使用HNSW或IVF索引提高检索速度
2. **缓存策略**: 实现查询结果缓存和热点数据缓存
3. **批量处理优化**: 优化文档批量上传和处理流程
4. **前端性能**: 代码分割、懒加载、图片优化

### 用户体验改进
1. **移动端适配**: 优化移动端界面
2. **快捷键支持**: 添加键盘快捷键提高操作效率
3. **主题切换**: 支持深色/浅色主题
4. **教程和引导**: 添加新用户引导和操作教程

## 许可证

MIT License
