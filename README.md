# MS-RAG: 昇腾性能定位指南 RAG 系统

基于 RAG 技术的昇腾 AI 计算平台性能问题智能问答系统，面向 MindStudio、msprof、算子性能、通信性能、快慢卡等场景，提供文档检索、结构化问答、来源引用、相关主题推荐和流式输出。

## 功能特性

- **文档处理与增量索引**：加载 `corpus/` 下 Markdown 文档，清洗文本、提取元数据和图片信息，按父子 chunk 构建索引，并通过文件 hash 跳过未变更文档。
- **混合检索**：Chroma 向量检索 + BM25 关键词检索，支持异步并发检索、重排序和父 chunk 回填。
- **知识图谱增强**：基于父子主题、兄弟主题和文档引用关系扩展检索结果，并返回相关主题推荐。
- **多级缓存**：L1 精确问答缓存、L2 语义相似问答缓存、L3 query embedding 缓存，支持统计查询和手动清理。
- **多 LLM 支持**：Claude、OpenAI、DeepSeek 可通过配置切换，支持自定义兼容 API base URL。
- **流式问答**：后端通过 SSE 推送 metadata、answer、done、error 事件，前端实时展示回答。
- **前端交互**：Vue 3 + TypeScript + Tailwind，支持快捷问题、Markdown 安全渲染、来源文档、图片和相关主题展示。

## 系统架构

```text
Vue 3 前端 / FastAPI 静态托管
        │
        ▼
FastAPI API 层
  ├─ /api/v1/qa
  ├─ /api/v1/qa/stream
  ├─ /api/v1/retrieve
  ├─ /api/v1/cache/stats
  └─ /api/v1/cache/clear
        │
        ▼
RAGPipeline
  ├─ CacheManager：L1 精确缓存 / L2 语义缓存 / L3 Embedding 缓存
  ├─ EmbeddingService：BAAI/bge-large-zh
  ├─ HybridRetriever：Chroma + BM25
  ├─ Reranker
  ├─ KnowledgeGraphEnhancer：父子/兄弟/引用扩展与相关主题
  ├─ ContextBuilder
  ├─ PromptTemplateManager
  └─ LLMService：anthropic / openai / deepseek
        │
        ▼
数据目录
  ├─ data/chroma/       Chroma 向量库（子 chunk）
  ├─ data/indexes/      BM25 索引
  ├─ data/docstore/     父 chunk 文档存储
  ├─ data/graph.json    文档关系图
  └─ data/index_state.json 增量索引状态
```

## 环境要求

- Python 3.10+
- Node.js 18+（前端开发或构建需要）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt

cd frontend
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

至少配置一个 LLM API Key：

```bash
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-6
LLM_API_KEY=your_api_key_here

# 也可使用 provider-specific key
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
DEEPSEEK_API_KEY=your_deepseek_key

# 如使用代理或兼容 API
LLM_BASE_URL=
```

### 3. 构建索引

```bash
python scripts/build_index.py
```

常用参数：

```bash
python scripts/build_index.py --force          # 强制重建全部索引
python scripts/build_index.py --corpus ./corpus --output ./data/chroma
```

构建过程会生成或更新：

- `data/chroma/`：Chroma 向量库
- `data/indexes/`：BM25 索引
- `data/docstore/doc_store.json`：父 chunk 文档存储
- `data/graph.json`：知识图谱增强使用的关系图
- `data/index_state.json`：增量索引状态

如果 HuggingFace 模型下载较慢，可使用镜像：

```bash
HF_ENDPOINT=https://hf-mirror.com python scripts/build_index.py
```

### 4. 启动服务

```bash
python -m src.main
```

访问：

- 前端界面：http://localhost:8000
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/v1/health

### 5. 前后端分离开发

```bash
# 终端 1：后端，端口 8000
python -m src.main

# 终端 2：前端，端口 3000
cd frontend
npm run dev
```

前端开发服务器会代理 `/api` 和 `/corpus` 请求到后端。

## API 接口

### 健康检查

```bash
curl http://localhost:8000/api/v1/health
```

返回向量库和 BM25 索引数量。

### 同步问答

```bash
curl -X POST http://localhost:8000/api/v1/qa \
  -H "Content-Type: application/json" \
  -d '{"query":"模型训练很慢，怎么定位问题？","options":{"top_k":5}}'
```

响应字段包含：

- `answer`：LLM 生成回答
- `question_type`：问题类型，如定位指导、问题诊断、工具使用
- `keywords`：关键词
- `sources`：来源文档
- `metadata.response_time_ms`：响应耗时
- `metadata.related_topics`：相关主题
- `metadata.cached/cache_level`：缓存命中信息（命中时出现）

### 流式问答 SSE

```bash
curl -N -X POST http://localhost:8000/api/v1/qa/stream \
  -H "Content-Type: application/json" \
  -d '{"query":"msprof 怎么分析通信耗时？"}'
```

事件类型：

- `metadata`：问题类型、关键词、来源文档、相关主题、缓存状态
- `answer`：回答文本增量片段
- `done`：响应耗时和模型信息
- `error`：错误信息

### 检索

```bash
curl -X POST http://localhost:8000/api/v1/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query":"msprof 工具使用","top_k":5}'
```

### 缓存统计

```bash
curl http://localhost:8000/api/v1/cache/stats
```

### 清理缓存

```bash
curl -X POST http://localhost:8000/api/v1/cache/clear \
  -H "Content-Type: application/json" \
  -d '{"level":"all"}'
```

`level` 支持 `all`、`l1`、`l2`、`l3`。

## 项目结构

```text
ms_rag/
├── config/
│   ├── system.yaml          # 系统、检索、缓存、知识图谱和 LLM 配置
│   ├── prompts.yaml         # Prompt 模板
│   └── logging.yaml         # 日志配置
├── src/
│   ├── api/                 # FastAPI 路由和 schema
│   ├── cache/               # L1/L2/L3 缓存实现
│   ├── core/                # 配置、日志、链路 tracing
│   ├── data/                # 文档加载、清洗、切分、元数据提取
│   ├── embeddings/          # Embedding 服务
│   ├── generation/          # LLM、Prompt、上下文构建
│   ├── pipeline/            # RAGPipeline
│   ├── retrieval/           # 混合检索、重排序、KG 增强
│   ├── storage/             # Chroma、BM25、DocumentStore
│   └── main.py              # 应用入口
├── frontend/                # Vue 3 前端
├── scripts/
│   ├── build_index.py       # 构建/增量更新索引
│   ├── evaluate.py          # 评估脚本
│   ├── test_api.py          # API 测试脚本
│   └── crawl_mindstudio.py  # MindStudio 文档爬取脚本
├── corpus/                  # Markdown 知识库语料
├── data/                    # 生成的索引、图谱和文档存储
├── docs/                    # 需求、设计和实施文档
├── static/                  # 前端生产构建产物
├── requirements.txt
└── pyproject.toml
```

## 配置说明

主要配置位于 `config/system.yaml`。

```yaml
embedding:
  model: "BAAI/bge-large-zh"
  device: "cpu"
  batch_size: 32
  normalize: true

retrieval:
  vector_weight: 0.6
  keyword_weight: 0.4
  top_k: 10
  rerank: true

llm:
  provider: "${LLM_PROVIDER:anthropic}"
  model: "${LLM_MODEL:claude-sonnet-4-6}"
  api_key: "${LLM_API_KEY}"
  base_url: "${LLM_BASE_URL:}"
  max_tokens: 2000
  temperature: 0.7

cache:
  enabled: true
  l1_max_size: 1000
  l1_ttl: 3600
  l2_max_size: 500
  l2_ttl: 1800
  l2_threshold: 0.92
  l3_max_size: 2000
  l3_ttl: 7200

knowledge_graph:
  enabled: true
  graph_path: "./data/graph.json"
  expand_parent: true
  expand_sibling: true
  expand_child: true
  expand_reference: true
  related_topics_count: 5
```

也可使用 `MS_RAG_` 前缀和 `__` 嵌套分隔符覆盖配置，例如：

```bash
MS_RAG_API__PORT=9000 python -m src.main
```

## 数据处理流程

```text
Markdown 语料
  ├─ DocumentLoader：加载文档、frontmatter、文件 hash
  ├─ TextCleaner：清洗正文
  ├─ DocumentSplitter：父 chunk + 子 chunk 切分
  ├─ DocumentStore：保存父 chunk 完整上下文
  ├─ EmbeddingService：对子 chunk 生成向量
  ├─ VectorStore：写入 Chroma
  ├─ BM25Index：构建关键词索引
  ├─ index_state.json：记录文件 hash 和 chunk id
  └─ graph.json：生成父子/引用关系图
```

在线问答时，系统先查缓存，再生成 query embedding，执行混合检索、父 chunk 回填、重排序、知识图谱增强、上下文构建和 LLM 生成。

## 常用开发命令

```bash
python -m src.main              # 启动后端
python scripts/build_index.py   # 增量构建索引
python scripts/build_index.py --force
pytest                          # 运行测试
ruff check .                    # 静态检查

cd frontend
npm run dev                     # 前端开发
npm run build                   # 类型检查并构建到 ../static
npm run preview                 # 预览前端构建
```

## 常见问题

### ModuleNotFoundError: No module named 'src'

请在仓库根目录执行 Python 命令，例如：

```bash
python -m src.main
python scripts/build_index.py
```

### 前端页面空白或不是最新版本

生产模式由后端托管 `static/`，需要重新构建前端：

```bash
cd frontend
npm run build
```

### LLM API 调用失败

检查 `.env` 中的 `LLM_API_KEY` 或 provider-specific key，并确认 `LLM_PROVIDER`、`LLM_MODEL`、`LLM_BASE_URL` 与所使用服务匹配。

### 索引没有反映语料更新

默认构建会根据文件 hash 增量更新。如需排除状态异常，执行：

```bash
python scripts/build_index.py --force
```

## 技术栈

| 模块 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 向量数据库 | Chroma |
| 关键词检索 | BM25 + jieba |
| Embedding | BAAI/bge-large-zh |
| 生成模型 | Claude / OpenAI / DeepSeek |
| 前端框架 | Vue 3 + TypeScript |
| 样式 | Tailwind CSS |
| Markdown 渲染 | marked + DOMPurify |
| 构建工具 | Vite |

## 许可证

MIT License
