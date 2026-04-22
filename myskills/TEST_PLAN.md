# MySkills 测试计划

## 测试环境

### 开发环境
- **操作系统**: Linux/Mac/Windows
- **Python**: 3.9+
- **Node.js**: 18+
- **依赖管理**: pip, npm

### 生产环境
- **Docker**: 20.10+
- **Docker Compose**: 1.29+

## 测试步骤

### 1. 环境准备

#### 开发环境
1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd myskills
   ```

2. **后端环境**
   ```bash
   cd backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **前端环境**
   ```bash
   cd frontend
   npm install
   ```

#### Docker环境
1. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑.env文件，配置必要的参数
   ```

2. **启动服务**
   ```bash
   docker-compose up -d
   ```

### 2. 功能测试

#### 后端API测试
1. **系统健康检查**
   ```bash
   curl http://localhost:8000/api/health
   # 预期响应: {"status": "healthy", "app_name": "MySkills Backend", "version": "1.0.0", "environment": "development"}
   ```

2. **知识库管理**
   ```bash
   # 创建知识库
   curl -X POST http://localhost:8000/api/knowledge-bases -H "Content-Type: application/json" -d '{"name": "测试知识库", "description": "测试用知识库"}'
   
   # 获取知识库列表
   curl http://localhost:8000/api/knowledge-bases
   ```

3. **文档管理**
   ```bash
   # 上传文档
   curl -X POST http://localhost:8000/api/knowledge-bases/{kb_id}/documents/upload -F "file=@test.txt"
   
   # 获取文档列表
   curl http://localhost:8000/api/knowledge-bases/{kb_id}/documents
   ```

4. **Excel文档管理**
   ```bash
   # 上传Excel文档
   curl -X POST http://localhost:8000/api/knowledge-bases/{kb_id}/excel-documents/upload -F "file=@test.xlsx"
   
   # 分块并存储
   curl -X POST http://localhost:8000/api/excel-documents/{doc_id}/chunk-and-store -H "Content-Type: application/json" -d '{"chunk_mode": "row_level"}'
   ```

5. **向量检索**
   ```bash
   # 测试检索
   curl -X POST http://localhost:8000/api/vectors/retrieve -H "Content-Type: application/json" -d '{"query": "测试查询", "knowledge_base_id": "{kb_id}"}'
   ```

6. **聊天功能**
   ```bash
   # 非流式聊天
   curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"query": "测试问题", "knowledge_base_id": "{kb_id}"}'
   
   # 流式聊天
   curl -X POST http://localhost:8000/api/chat/stream -H "Content-Type: application/json" -d '{"query": "测试问题", "knowledge_base_id": "{kb_id}"}'
   ```

#### 前端功能测试
1. **访问前端**
   - 打开浏览器访问: http://localhost:5173

2. **仪表盘**
   - 检查统计数据显示
   - 测试快速访问链接

3. **知识库管理**
   - 创建、编辑、删除知识库
   - 查看知识库详情
   - 生成知识库摘要

4. **文档管理**
   - 上传不同格式的文档
   - 创建Markdown文档
   - 查看文档详情
   - 删除文档

5. **Excel文档管理**
   - 上传Excel文件
   - 配置分块模式
   - 预览分块效果
   - 分块并存储

6. **向量管理**
   - 测试向量检索
   - 重建向量索引
   - 查看向量列表

7. **AI对话**
   - 发送聊天消息
   - 测试流式响应
   - 选择知识库
   - 查看回答来源

8. **Skill配置**
   - 配置Function Calling参数
   - 调整检索参数
   - 查看Function Calling元数据

9. **调试面板**
   - 测试Skill调用
   - 查看检索结果

10. **智能体模板**
    - 查看智能体模板列表
    - 查看模板详情

### 3. 性能测试

1. **文档上传性能**
   - 测试不同大小文档的上传时间
   - 测试批量文档上传

2. **向量检索性能**
   - 测试不同查询的响应时间
   - 测试不同知识库大小的检索性能

3. **聊天响应性能**
   - 测试非流式响应时间
   - 测试流式响应的首字时间

### 4. 兼容性测试

1. **浏览器兼容性**
   - Chrome
   - Firefox
   - Safari
   - Edge

2. **设备兼容性**
   - 桌面端
   - 平板端
   - 移动端

3. **数据库兼容性**
   - SQLite
   - PostgreSQL

### 5. 安全测试

1. **文件上传安全**
   - 测试文件大小限制
   - 测试文件类型验证

2. **API安全**
   - 测试CORS配置
   - 测试输入验证

3. **数据安全**
   - 测试敏感信息处理
   - 测试文件存储安全

## 测试结果记录

| 测试项 | 预期结果 | 实际结果 | 状态 | 备注 |
|--------|----------|----------|------|------|
| 系统健康检查 | 正常响应 | | | |
| 知识库创建 | 成功创建 | | | |
| 文档上传 | 成功上传 | | | |
| Excel分块 | 成功分块 | | | |
| 向量检索 | 正确检索 | | | |
| AI对话 | 正确回答 | | | |
| 前端界面 | 正常加载 | | | |
| 性能测试 | 响应及时 | | | |
| 兼容性测试 | 正常运行 | | | |
| 安全测试 | 无安全问题 | | | |

## 故障排除

### 常见问题及解决方案

1. **嵌入模型下载失败**
   - 检查网络连接
   - 配置HF_ENDPOINT镜像: `export HF_ENDPOINT=https://hf-mirror.com`

2. **向量检索效果差**
   - 调整分块大小和重叠参数
   - 尝试更换嵌入模型

3. **内存不足**
   - 减少批量处理大小
   - 使用GPU加速（设置EMBEDDING_DEVICE=cuda）

4. **文件上传失败**
   - 检查文件大小是否超过限制
   - 检查文件格式是否支持

5. **数据库连接失败**
   - 检查数据库URL配置
   - 检查数据库服务是否运行

6. **Docker启动失败**
   - 检查Docker服务是否运行
   - 检查端口是否被占用
   - 检查环境变量配置

## 测试结论

- [ ] 所有功能正常运行
- [ ] 性能符合预期
- [ ] 兼容性良好
- [ ] 安全无问题

## 后续建议

1. **自动化测试**
   - 编写单元测试
   - 编写集成测试
   - 配置CI/CD流程

2. **性能优化**
   - 优化向量检索速度
   - 优化文档处理流程
   - 优化前端加载速度

3. **功能增强**
   - 添加更多文件格式支持
   - 增强Excel分块功能
   - 添加用户认证系统
