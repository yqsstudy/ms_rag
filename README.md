# MS-RAG: 性能定位指南RAG系统

基于RAG技术的昇腾AI计算平台性能问题智能问答系统。

## 功能特性

- 📄 **智能文档处理**：自动切分、清洗、元数据提取、图片信息提取
- 🔍 **混合检索**：向量检索 + BM25关键词检索 + 重排序
- 🤖 **多LLM支持**：Claude / OpenAI / DeepSeek 可切换
- 🌊 **流式输出**：支持SSE流式响应
- 🖼️ **图片展示**：回答中展示相关图片
- ⚡ **高性能**：响应时间 < 3秒

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      前端 (Vue 3 + Tailwind)                │
│                    http://localhost:8000                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    后端 API (FastAPI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  问答接口    │  │  检索接口    │  │  流式接口    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      RAG Pipeline                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  混合检索    │  │  重排序      │  │  LLM生成     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据存储                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Chroma      │  │  BM25索引    │  │  文档语料    │      │
│  │  (向量库)    │  │  (关键词)    │  │  (41个文档)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+ (仅前端开发需要)

### 1. 安装依赖

```bash
# 后端依赖
pip install -r requirements.txt

# 前端依赖 (可选，仅开发时需要)
cd frontend
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置 LLM API Key：

```bash
# 选择一个提供商设置 API Key
LLM_API_KEY=your_api_key_here

# 或者设置提供商特定的 Key
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
DEEPSEEK_API_KEY=your_deepseek_key
```

### 3. 构建索引

```bash
python scripts/build_index.py
```

输出示例：
```
Loaded 41 documents
Created 136 chunks
Generated 136 embeddings
Stored 136 chunks in vector store
Built BM25 index with 136 documents
```

### 4. 构建前端 (生产模式)

```bash
cd frontend
npm install
npm run build
```

### 5. 启动服务

```bash
python -m src.main
```

服务启动后访问：
- **前端界面**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/api/v1/health

## 开发模式

### 前后端分离开发

```bash
# 终端1: 启动后端 (端口 8000)
python -m src.main

# 终端2: 启动前端开发服务器 (端口 3000)
cd frontend
npm run dev
```

访问 http://localhost:3000，前端会自动代理 API 请求到后端。

## API 接口

### 问答接口 (同步)

```bash
curl -X POST http://localhost:8000/api/v1/qa \
  -H "Content-Type: application/json" \
  -d '{"query": "模型训练很慢，怎么定位问题？"}'
```

响应示例：
```json
{
  "code": 0,
  "data": {
    "answer": "针对模型训练速度慢的问题，建议按以下步骤定位...",
    "question_type": "定位指导",
    "sources": [
      {
        "doc_id": "toolsample6_003",
        "title": "性能问题的定位流程",
        "relevance_score": 0.92
      }
    ]
  }
}
```

### 问答接口 (流式 SSE)

```bash
curl -X POST http://localhost:8000/api/v1/qa/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "模型训练很慢，怎么定位问题？"}'
```

### 检索接口

```bash
curl -X POST http://localhost:8000/api/v1/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "msprof工具使用", "top_k": 5}'
```

### 健康检查

```bash
curl http://localhost:8000/api/v1/health
```

响应：
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "vector_store_count": 136,
  "keyword_index_count": 136
}
```

## 项目结构

```
ms_rag/
├── config/                   # 配置文件
│   ├── system.yaml          # 系统配置
│   ├── prompts.yaml         # Prompt模板
│   └── logging.yaml         # 日志配置
│
├── src/                     # 源代码
│   ├── core/                # 核心配置
│   │   ├── config.py        # 配置管理
│   │   └── logging.py       # 日志配置
│   │
│   ├── data/                # 数据处理
│   │   ├── loader.py        # 文档加载
│   │   ├── splitter.py      # 文档切分
│   │   ├── cleaner.py       # 文本清洗
│   │   └── metadata.py      # 元数据提取
│   │
│   ├── embeddings/          # 向量化
│   │   └── embedding.py     # Embedding服务
│   │
│   ├── storage/             # 存储
│   │   ├── vector_store.py  # Chroma向量库
│   │   └── keyword_index.py # BM25索引
│   │
│   ├── retrieval/           # 检索
│   │   ├── hybrid_retriever.py  # 混合检索
│   │   └── reranker.py      # 重排序
│   │
│   ├── generation/          # 生成
│   │   ├── llm_service.py   # LLM服务
│   │   ├── prompt_templates.py  # Prompt模板
│   │   └── context_builder.py   # 上下文构建
│   │
│   ├── pipeline/            # RAG流水线
│   │   └── rag_pipeline.py
│   │
│   ├── api/                 # API接口
│   │   ├── routes.py        # 路由
│   │   └── schemas.py       # 数据模型
│   │
│   └── main.py              # 应用入口
│
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── components/      # Vue组件
│   │   ├── composables/     # 组合式函数
│   │   └── types/           # TypeScript类型
│   └── package.json
│
├── scripts/                 # 脚本
│   ├── build_index.py       # 构建索引
│   └── test_api.py          # API测试
│
├── tests/                   # 测试
│
├── data/                    # 数据目录
│   ├── chroma/              # Chroma数据
│   └── indexes/             # 索引文件
│
├── corpus/                  # 文档语料
│   └── performance_guide/   # 性能指南文档
│
├── docs/                    # 文档
│   ├── requirements.md      # 需求文档
│   ├── system_design.md     # 系统设计
│   ├── frontend_design.md   # 前端设计
│   └── task_breakdown.md    # 任务拆分
│
├── static/                  # 前端构建产物
│
├── requirements.txt         # Python依赖
└── README.md
```

## 配置说明

编辑 `config/system.yaml` 进行配置：

```yaml
# LLM配置
llm:
  provider: "anthropic"  # anthropic | openai | deepseek
  model: "claude-sonnet-4-6"
  max_tokens: 2000
  temperature: 0.7

# Embedding配置
embedding:
  model: "BAAI/bge-large-zh"
  device: "cpu"  # cpu | cuda | mps

# 检索配置
retrieval:
  vector_weight: 0.6
  keyword_weight: 0.4
  top_k: 10
  rerank: true

# 文档处理配置
document:
  min_chunk_size: 1500
  max_chunk_size: 2000
  chunk_overlap: 200
```

## 数据处理流程

```
原始文档 (Markdown)
    │
    ├── 文档加载 (loader.py)
    │   └── 解析YAML frontmatter
    │
    ├── 文本清洗 (cleaner.py)
    │   └── 移除HTML、规范化空白
    │
    ├── 文档切分 (splitter.py)
    │   ├── 按标题切分
    │   ├── 处理过长章节
    │   └── 添加重叠内容
    │
    ├── 图片提取
    │   └── 提取图片标题和路径
    │
    ├── 向量化 (embedding.py)
    │   └── bge-large-zh (1024维)
    │
    └── 存储
        ├── Chroma向量库
        └── BM25索引
```

## 常见问题

### 1. 模型下载慢

bge-large-zh 模型约 1.3GB，首次运行需要下载。可以使用镜像站：

```bash
export HF_ENDPOINT=https://hf-mirror.com
python scripts/build_index.py
```

### 2. ModuleNotFoundError: No module named 'src'

确保在项目根目录执行命令，或使用：

```bash
python -m scripts.build_index
```

### 3. LLM API 调用失败

检查 `.env` 文件中的 API Key 是否正确配置。

### 4. 前端页面空白

确保已构建前端：

```bash
cd frontend
npm run build
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| RAG框架 | LangChain |
| 向量数据库 | Chroma |
| 关键词检索 | BM25 + jieba |
| Embedding | bge-large-zh |
| LLM | Claude / OpenAI / DeepSeek |
| 前端框架 | Vue 3 + TypeScript |
| 样式 | Tailwind CSS |
| 构建工具 | Vite |

## 许可证

MIT License
