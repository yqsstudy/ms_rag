# 性能定位指南RAG系统设计文档

## 一、系统概述

### 1.1 设计目标

基于需求文档，设计一个能够帮助昇腾开发者快速定位和解决性能问题的智能问答系统。系统采用RAG（Retrieval-Augmented Generation）架构，结合向量检索和关键词检索，为用户提供准确、专业的解决方案。

### 1.2 设计原则

- **模块化设计**：各组件解耦，便于独立升级和替换
- **渐进式实现**：支持从MVP到生产环境的平滑演进
- **可配置性**：关键参数可通过配置文件调整
- **可观测性**：完善的日志和监控支持

### 1.3 系统架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户交互层                                │
│                    (REST API / 前端界面)                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         应用服务层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  问答服务    │  │  检索服务    │  │  生成服务    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         核心引擎层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  混合检索引擎 │  │  重排序引擎  │  │  Prompt引擎  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         数据存储层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  向量数据库   │  │  文档索引    │  │  元数据存储  │          │
│  │  (Chroma)    │  │  (BM25)     │  │  (JSON/DB)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         数据处理层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  文档切分    │  │  向量化      │  │  索引构建    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、系统架构设计

### 2.1 整体架构

系统采用分层架构，从下到上分为：

1. **数据处理层**：负责文档预处理、切分、向量化
2. **数据存储层**：存储向量、索引、元数据
3. **核心引擎层**：实现检索、重排序、Prompt生成
4. **应用服务层**：提供问答、检索、生成服务
5. **用户交互层**：API接口和可选的前端界面

### 2.2 数据流设计

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 原始文档  │───▶│ 文档切分  │───▶│ 向量化   │───▶│ 索引存储  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘

┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 用户问题  │───▶│ 问题处理  │───▶│ 混合检索  │───▶│ 重排序   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                      │
┌──────────┐    ┌──────────┐    ┌──────────┐         │
│ 返回答案  │◀───│ LLM生成  │◀───│ 构建上下文 │◀────────┘
└──────────┘    └──────────┘    └──────────┘
```

---

## 三、模块详细设计

### 3.1 数据处理模块

#### 3.1.1 文档切分器 (DocumentSplitter)

**职责**：将原始Markdown文档切分成适合检索的chunks

**输入**：原始Markdown文档（含YAML frontmatter）

**输出**：Chunk列表，每个Chunk包含：
- chunk_id: 唯一标识
- title: 章节标题
- content: 正文内容
- metadata: 元数据（文档标题、父主题、来源URL等）
- images: 图片描述列表

**切分策略**：

```python
class ChunkingStrategy:
    """
    切分策略：
    1. 按 #### 标题切分成独立chunks
    2. 过长章节（>2000字符）按段落二次切分
    3. 过短文档（<1500字符）保持完整
    """

    MIN_CHUNK_SIZE = 1500  # 字符
    MAX_CHUNK_SIZE = 2000  # 字符
    HEADING_PATTERN = r'^#{1,4}\s+'  # 标题正则
```

**处理流程**：

```
原始文档
    │
    ▼
解析YAML frontmatter ──▶ 提取元数据
    │
    ▼
按标题切分 ──▶ 生成初始chunks
    │
    ▼
检查chunk大小
    │
    ├── 过长(>2000) ──▶ 按段落二次切分
    ├── 过短(<1500) ──▶ 保持完整或合并
    └── 适中 ──▶ 保持原样
    │
    ▼
提取图片描述 ──▶ 附加到chunk
    │
    ▼
输出chunks列表
```

#### 3.1.2 元数据提取器 (MetadataExtractor)

**职责**：从文档中提取结构化元数据

**提取内容**：

| 字段 | 来源 | 说明 |
|------|------|------|
| doc_title | YAML frontmatter.title | 文档标题 |
| source_url | YAML frontmatter.source | 来源URL |
| parent_topic | 文档末尾"父主题" | 父主题关系 |
| section_title | Markdown标题 | 章节标题 |
| images | 图片标记 | 图片标题列表 |
| links | 超链接 | 跨文档链接 |

#### 3.1.3 文本清洗器 (TextCleaner)

**职责**：清理文档中的噪声内容

**清洗规则**：

```python
class CleaningRule:
    REMOVE_HTML_TAGS = True      # 移除HTML残留
    NORMALIZE_WHITESPACE = True  # 规范化空白
    FIX_ENCODING = True          # 修复编码问题
    REMOVE_EMPTY_LINES = True    # 移除空行
```

### 3.2 向量化模块

#### 3.2.1 Embedding服务

**职责**：将文本转换为向量表示

**模型选择**：

| 阶段 | 模型 | 部署方式 | 维度 |
|------|------|----------|------|
| Phase 1-2 | bge-large-zh | 本地部署 | 1024 |
| Phase 3-4 | bge-large-zh / OpenAI | 本地/云端 | 1024/1536 |

**接口设计**：

```python
class EmbeddingService:
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """批量文本向量化"""
        pass

    def embed_query(self, query: str) -> List[float]:
        """单个查询向量化"""
        pass
```

**性能考虑**：
- 批量处理提高效率
- 缓存常用查询的向量
- 支持异步处理

### 3.3 存储模块

#### 3.3.1 向量数据库 (VectorStore)

**职责**：存储和检索向量化的文档chunks

**Phase 1-2 选型：Chroma**

```python
class ChromaVectorStore:
    def __init__(self, persist_directory: str):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="performance_guide",
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: List[Chunk], embeddings: List[List[float]]):
        """添加文档chunks"""
        pass

    def similarity_search(self, query_embedding: List[float], k: int = 5) -> List[SearchResult]:
        """向量相似度检索"""
        pass
```

**Phase 3-4 迁移：Milvus**

```python
class MilvusVectorStore:
    # 支持分布式部署
    # 支持更大规模数据
    # 支持更复杂的查询
```

#### 3.3.2 关键词索引 (KeywordIndex)

**职责**：支持基于BM25的关键词检索

**实现方案**：使用 `rank_bm25` 库

```python
class BM25Index:
    def __init__(self):
        self.tokenizer = ChineseTokenizer()  # 中文分词
        self.bm25 = None

    def build_index(self, chunks: List[Chunk]):
        """构建BM25索引"""
        corpus = [self.tokenizer.tokenize(c.content) for c in chunks]
        self.bm25 = BM25Okapi(corpus)

    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        """关键词检索"""
        pass
```

#### 3.3.3 元数据存储 (MetadataStore)

**职责**：存储文档元数据和知识图谱关系

**存储内容**：

```json
{
  "doc_id": "toolsample6_002",
  "title": "概述",
  "source_url": "https://...",
  "parent_topic": "toolsample6_001",
  "child_topics": ["toolsample6_003", "toolsample6_005"],
  "keywords": ["性能优化", "算子", "通信"],
  "images": [
    {"id": "img_001", "caption": "性能优化流程图"}
  ]
}
```

### 3.4 检索模块

#### 3.4.1 混合检索器 (HybridRetriever)

**职责**：结合向量检索和关键词检索

**检索策略**：

```python
class HybridRetriever:
    def __init__(self, vector_store, keyword_index, config):
        self.vector_store = vector_store
        self.keyword_index = keyword_index
        self.vector_weight = config.get('vector_weight', 0.6)
        self.keyword_weight = config.get('keyword_weight', 0.4)

    def retrieve(self, query: str, k: int = 5) -> List[SearchResult]:
        # 1. 向量检索
        vector_results = self.vector_store.search(query, k=k*2)

        # 2. 关键词检索
        keyword_results = self.keyword_index.search(query, k=k*2)

        # 3. 融合排序
        merged = self._merge_results(vector_results, keyword_results)

        return merged[:k]

    def _merge_results(self, vector_results, keyword_results) -> List[SearchResult]:
        """RRF (Reciprocal Rank Fusion) 融合算法"""
        pass
```

**权重配置**：

| 问题类型 | 向量权重 | 关键词权重 |
|----------|----------|------------|
| 概念理解 | 0.7 | 0.3 |
| 工具使用 | 0.5 | 0.5 |
| 问题诊断 | 0.6 | 0.4 |
| 定位指导 | 0.6 | 0.4 |

#### 3.4.2 重排序器 (Reranker)

**职责**：对检索结果进行精细化排序

**排序因素**：

```python
class Reranker:
    def rerank(self, query: str, results: List[SearchResult]) -> List[SearchResult]:
        scores = []
        for result in results:
            score = 0.0
            score += self._semantic_score(query, result) * 0.4
            score += self._keyword_match_score(query, result) * 0.3
            score += self._authority_score(result) * 0.2
            score += self._completeness_score(result) * 0.1
            result.final_score = score
        return sorted(results, key=lambda x: x.final_score, reverse=True)
```

**文档权威性评分**：

| 文档类型 | 权威性分数 |
|----------|------------|
| 概述/简介 | 1.0 |
| 定位流程 | 0.9 |
| 工具使用 | 0.9 |
| 问题解决方案 | 0.8 |
| 案例分析 | 0.7 |

#### 3.4.3 知识图谱增强 (KnowledgeGraphEnhancer)

**职责**：利用文档结构关系增强检索

**增强策略**：

```python
class KnowledgeGraphEnhancer:
    def enhance_results(self, results: List[SearchResult]) -> List[SearchResult]:
        enhanced = []
        for result in results:
            # 1. 添加父文档上下文
            parent_context = self._get_parent_context(result.doc_id)

            # 2. 添加相关文档链接
            related_docs = self._get_related_docs(result.doc_id)

            # 3. 扩展结果
            result.parent_context = parent_context
            result.related_docs = related_docs
            enhanced.append(result)

        return enhanced
```

### 3.5 生成模块

#### 3.5.1 Prompt模板管理器

**职责**：管理和渲染不同类型的Prompt模板

**模板类型**：

```python
class PromptTemplateManager:
    templates = {
        "定位指导": """
你是一位昇腾AI计算平台的性能优化专家。用户遇到了性能问题，需要你提供系统化的定位指导。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 问题分析
2. 定位步骤
3. 推荐工具
4. 注意事项

回答时请引用相关文档来源。
""",
        "问题诊断": """
你是一位昇腾AI计算平台的性能优化专家。用户遇到了具体的性能问题，需要你帮助诊断原因。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 问题原因分析
2. 可能的影响
3. 定位方法
4. 解决建议

回答时请引用相关文档来源。
""",
        "工具使用": """
你是一位昇腾AI计算平台的性能优化专家。用户需要了解工具的使用方法。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 工具简介
2. 使用命令/步骤
3. 参数说明
4. 结果解读
5. 示例（如有）

回答时请引用相关文档来源。
""",
        "概念理解": """
你是一位昇腾AI计算平台的性能优化专家。用户需要理解某个概念。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 概念定义
2. 影响说明
3. 相关场景
4. 解决方法（如适用）

回答时请引用相关文档来源。
"""
    }
```

#### 3.5.2 上下文构建器 (ContextBuilder)

**职责**：构建LLM输入的上下文

**构建策略**：

```python
class ContextBuilder:
    MAX_CONTEXT_TOKENS = 4000  # 上下文token限制

    def build_context(self, query: str, results: List[SearchResult]) -> str:
        context_parts = []
        current_tokens = 0

        for result in results:
            chunk_text = self._format_chunk(result)
            chunk_tokens = self._count_tokens(chunk_text)

            if current_tokens + chunk_tokens > self.MAX_CONTEXT_TOKENS:
                break

            context_parts.append(chunk_text)
            current_tokens += chunk_tokens

        return "\n\n---\n\n".join(context_parts)

    def _format_chunk(self, result: SearchResult) -> str:
        return f"""【文档】{result.doc_title}
【章节】{result.section_title}
【内容】{result.content}
【来源】{result.source_url}
"""
```

#### 3.5.3 LLM服务 (LLMService)

**职责**：调用LLM生成回答，支持多提供商切换

**接口设计**：

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """LLM提供商抽象接口"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """同步生成回答"""
        pass

    @abstractmethod
    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """流式生成回答"""
        pass


class AnthropicProvider(LLMProvider):
    """Claude API 实现"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get('max_tokens', 2000),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        with self.client.messages.stream(
            model=self.model,
            max_tokens=kwargs.get('max_tokens', 2000),
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text


class OpenAIProvider(LLMProvider):
    """OpenAI API 实现"""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get('max_tokens', 2000)
        )
        return response.choices[0].message.content

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get('max_tokens', 2000),
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class DeepSeekProvider(LLMProvider):
    """DeepSeek API 实现"""

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = model

    # 实现同OpenAI...


class LLMService:
    """LLM服务统一入口"""

    PROVIDERS = {
        "anthropic": AnthropicProvider,
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
    }

    def __init__(self, config: LLMConfig):
        provider_class = self.PROVIDERS.get(config.provider)
        if not provider_class:
            raise ValueError(f"Unknown provider: {config.provider}")
        self.provider = provider_class(config.api_key, config.model)
        self.config = config

    def generate(self, prompt: str, **kwargs) -> str:
        """同步生成回答"""
        return self.provider.generate(prompt, **kwargs)

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """流式生成回答"""
        return self.provider.generate_stream(prompt, **kwargs)
```

**模型配置**：

| 提供商 | 模型 | 特点 | 适用场景 |
|--------|------|------|----------|
| Anthropic | claude-sonnet-4-6 | 效果好，中文能力强 | 开发验证、高质量回答 |
| OpenAI | gpt-4-turbo | 生态成熟，稳定 | 备选方案 |
| DeepSeek | deepseek-chat | 成本低，中文效果好 | 生产环境降本 |

**配置切换**：

```yaml
# config/system.yaml
llm:
  provider: "anthropic"  # anthropic | openai | deepseek
  model: "claude-sonnet-4-6"
  api_key: "${LLM_API_KEY}"  # 从环境变量读取
  max_tokens: 2000
  temperature: 0.7
```

### 3.6 问答服务模块

#### 3.6.1 问答服务 (QAService)

**职责**：协调各模块完成问答流程

**核心流程**：

```python
class QAService:
    def __init__(self,
                 query_processor: QueryProcessor,
                 retriever: HybridRetriever,
                 reranker: Reranker,
                 context_builder: ContextBuilder,
                 llm_service: LLMService,
                 prompt_manager: PromptTemplateManager):
        self.query_processor = query_processor
        self.retriever = retriever
        self.reranker = reranker
        self.context_builder = context_builder
        self.llm_service = llm_service
        self.prompt_manager = prompt_manager

    def answer(self, query: str, **options) -> QAResponse:
        # 1. 问题处理
        processed_query = self.query_processor.process(query)
        question_type = processed_query.type
        keywords = processed_query.keywords

        # 2. 检索
        results = self.retriever.retrieve(query, k=10)

        # 3. 重排序
        reranked_results = self.reranker.rerank(query, results)

        # 4. 构建上下文
        context = self.context_builder.build_context(query, reranked_results[:5])

        # 5. 生成Prompt
        prompt = self.prompt_manager.render(question_type, query=query, context=context)

        # 6. LLM生成
        answer = self.llm_service.generate(prompt)

        # 7. 构建响应
        return QAResponse(
            answer=answer,
            sources=[r.to_dict() for r in reranked_results[:5]],
            question_type=question_type,
            keywords=keywords
        )
```

#### 3.6.2 问题处理器 (QueryProcessor)

**职责**：分析用户问题，提取关键信息

**处理内容**：

```python
class QueryProcessor:
    def process(self, query: str) -> ProcessedQuery:
        return ProcessedQuery(
            original=query,
            normalized=self._normalize(query),
            type=self._classify(query),
            keywords=self._extract_keywords(query),
            entities=self._extract_entities(query)
        )

    def _classify(self, query: str) -> str:
        """问题分类"""
        # 使用规则或小模型分类
        # 返回: "定位指导" | "问题诊断" | "工具使用" | "概念理解" | "操作步骤"
        pass

    def _extract_keywords(self, query: str) -> List[str]:
        """关键词提取"""
        # 提取专业术语: msprof, 通信, 快慢卡, Host Bound等
        pass
```

---

## 四、API接口设计

### 4.1 REST API

#### 4.1.1 问答接口（同步）

**请求**：

```http
POST /api/v1/qa
Content-Type: application/json

{
  "query": "模型训练很慢，怎么定位问题？",
  "options": {
    "top_k": 5,
    "include_sources": true,
    "question_type": null
  }
}
```

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "answer": "针对模型训练速度慢的问题，建议按以下步骤定位...",
    "question_type": "定位指导",
    "keywords": ["训练", "定位", "性能"],
    "sources": [
      {
        "doc_id": "toolsample6_003",
        "title": "性能问题的定位流程",
        "section": "定位步骤",
        "source_url": "https://...",
        "relevance_score": 0.92
      }
    ],
    "related_links": [
      {
        "title": "性能工具的使用",
        "url": "https://..."
      }
    ]
  },
  "metadata": {
    "response_time_ms": 1234,
    "model": "claude-sonnet-4-6",
    "tokens_used": 1500
  }
}
```

#### 4.1.2 问答接口（流式 SSE）

**请求**：

```http
POST /api/v1/qa/stream
Content-Type: application/json

{
  "query": "模型训练很慢，怎么定位问题？",
  "options": {
    "top_k": 5,
    "include_sources": true
  }
}
```

**响应（SSE格式）**：

```
event: metadata
data: {"question_type": "定位指导", "keywords": ["训练", "定位"], "sources": [...]}

event: answer
data: {"content": "针对模型训练速度慢的问题，"}

event: answer
data: {"content": "建议按以下步骤定位："}

event: answer
data: {"content": "1. 首先使用msprof工具采集性能数据..."}

event: done
data: {"tokens_used": 1500, "response_time_ms": 1234}
```

**前端调用示例**：

```javascript
const eventSource = new EventSource('/api/v1/qa/stream', {
  method: 'POST',
  body: JSON.stringify({ query: '模型训练很慢' })
});

eventSource.addEventListener('metadata', (e) => {
  const data = JSON.parse(e.data);
  // 显示问题类型、来源文档
});

eventSource.addEventListener('answer', (e) => {
  const data = JSON.parse(e.data);
  // 逐步显示回答内容
});

eventSource.addEventListener('done', (e) => {
  eventSource.close();
});
```

#### 4.1.2 检索接口

**请求**：

```http
POST /api/v1/retrieve
Content-Type: application/json

{
  "query": "msprof工具使用",
  "top_k": 10,
  "retrieval_type": "hybrid"
}
```

**响应**：

```json
{
  "code": 0,
  "data": {
    "results": [
      {
        "chunk_id": "toolsample6_009_chunk_1",
        "doc_title": "性能工具的使用",
        "section_title": "msprof工具介绍",
        "content": "msprof是昇腾性能分析工具...",
        "source_url": "https://...",
        "score": 0.95
      }
    ],
    "total": 10
  }
}
```

#### 4.1.3 文档列表接口

**请求**：

```http
GET /api/v1/documents
```

**响应**：

```json
{
  "code": 0,
  "data": {
    "documents": [
      {
        "doc_id": "toolsample6_001",
        "title": "文档简介",
        "parent_topic": null,
        "child_topics": ["toolsample6_002", "toolsample6_003"],
        "chunk_count": 3,
        "source_url": "https://..."
      }
    ],
    "total": 41
  }
}
```

### 4.2 错误响应

```json
{
  "code": 1001,
  "message": "查询内容不能为空",
  "data": null
}
```

**错误码定义**：

| 错误码 | 说明 |
|--------|------|
| 1001 | 请求参数错误 |
| 1002 | 查询内容为空 |
| 2001 | 向量库连接失败 |
| 2002 | LLM服务不可用 |
| 3001 | 未找到相关文档 |

---

## 五、数据模型设计

### 5.1 核心数据结构

#### Chunk

```python
@dataclass
class Chunk:
    chunk_id: str           # 唯一标识
    doc_id: str             # 文档ID
    doc_title: str          # 文档标题
    section_title: str      # 章节标题
    content: str            # 正文内容
    source_url: str         # 来源URL
    parent_topic: str       # 父主题
    images: List[ImageRef]  # 图片引用
    keywords: List[str]     # 关键词
    embedding: List[float]  # 向量（可选存储）
```

#### SearchResult

```python
@dataclass
class SearchResult:
    chunk_id: str
    doc_id: str
    doc_title: str
    section_title: str
    content: str
    source_url: str
    score: float            # 检索得分
    final_score: float      # 重排序后得分
    parent_context: str     # 父文档上下文
    related_docs: List[str] # 相关文档ID
```

#### QAResponse

```python
@dataclass
class QAResponse:
    answer: str                         # 生成的回答
    sources: List[Dict]                 # 来源文档
    question_type: str                  # 问题类型
    keywords: List[str]                 # 提取的关键词
    related_links: List[Dict]           # 相关链接
    metadata: Dict                      # 元数据
```

### 5.2 配置数据结构

#### 系统配置

```yaml
# config/system.yaml
embedding:
  model: "bge-large-zh"
  device: "cpu"  # cpu | cuda
  batch_size: 32

vector_store:
  type: "chroma"
  persist_directory: "./data/chroma"
  collection_name: "performance_guide"

retrieval:
  vector_weight: 0.6
  keyword_weight: 0.4
  top_k: 10

llm:
  provider: "anthropic"
  model: "claude-sonnet-4-6"
  api_key: "${ANTHROPIC_API_KEY}"
  max_tokens: 2000
  temperature: 0.7

api:
  host: "0.0.0.0"
  port: 8000
  debug: false
```

---

## 六、项目结构设计

```
ms_rag/
├── config/                     # 配置文件
│   ├── system.yaml            # 系统配置
│   ├── prompts.yaml           # Prompt模板配置
│   └── logging.yaml           # 日志配置
│
├── src/                       # 源代码
│   ├── __init__.py
│   ├── main.py                # 应用入口
│   │
│   ├── core/                  # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py          # 配置管理
│   │   └── logging.py         # 日志配置
│   │
│   ├── data/                  # 数据处理模块
│   │   ├── __init__.py
│   │   ├── loader.py          # 文档加载器
│   │   ├── splitter.py        # 文档切分器
│   │   ├── cleaner.py         # 文本清洗器
│   │   └── metadata.py        # 元数据提取器
│   │
│   ├── embeddings/            # 向量化模块
│   │   ├── __init__.py
│   │   └── embedding.py       # Embedding服务
│   │
│   ├── storage/               # 存储模块
│   │   ├── __init__.py
│   │   ├── vector_store.py    # 向量数据库
│   │   └── keyword_index.py   # 关键词索引
│   │
│   ├── retrieval/             # 检索模块
│   │   ├── __init__.py
│   │   ├── hybrid_retriever.py    # 混合检索器
│   │   └── reranker.py        # 重排序器
│   │
│   ├── generation/            # 生成模块
│   │   ├── __init__.py
│   │   ├── llm_service.py     # LLM服务（多提供商）
│   │   ├── prompt_templates.py    # Prompt模板
│   │   └── context_builder.py # 上下文构建
│   │
│   ├── pipeline/              # LangChain流水线
│   │   ├── __init__.py
│   │   └── rag_pipeline.py    # RAG流水线
│   │
│   └── api/                   # API层
│       ├── __init__.py
│       ├── routes.py          # 路由定义
│       ├── qa_routes.py       # 问答路由（含SSE）
│       ├── schemas.py         # 请求/响应模型
│       └── middleware.py      # 中间件
│
├── scripts/                   # 脚本
│   ├── build_index.py         # 构建索引
│   ├── evaluate.py            # 评估脚本
│   └── test_api.py            # API测试
│
├── tests/                     # 测试
│   ├── test_splitter.py
│   ├── test_retrieval.py
│   └── test_qa.py
│
├── data/                      # 数据目录
│   ├── chroma/                # Chroma数据
│   ├── indexes/               # 索引文件
│   └── cache/                 # 缓存
│
├── corpus/                    # 原始文档
│   └── performance_guide/
│
├── docs/                      # 文档
│   ├── requirements.md
│   └── system_design.md
│
├── requirements.txt           # 依赖
├── pyproject.toml            # 项目配置
└── README.md
```

---

## 七、技术选型

### 7.1 Phase 1-2 技术栈

| 组件 | 技术选型 | 说明 |
|------|----------|------|
| 编程语言 | Python 3.10+ | 生态丰富 |
| Web框架 | FastAPI | 高性能，自动文档，原生支持SSE |
| RAG框架 | LangChain | 生态丰富，社区活跃，模块化设计 |
| Embedding | bge-large-zh | 中文效果好，本地部署 |
| 向量数据库 | Chroma | 轻量级，快速验证，LangChain集成 |
| 关键词检索 | rank_bm25 | BM25算法实现 |
| 中文分词 | jieba | 成熟的中文分词库 |
| LLM | 可切换（Claude/OpenAI/DeepSeek） | 多提供商支持 |
| 配置管理 | Pydantic + YAML | 类型安全 |

### 7.2 LangChain集成设计

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document

class LangChainRAGPipeline:
    """基于LangChain的RAG流水线"""

    def __init__(self, config: Config):
        # 1. Embedding模型
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-zh",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        # 2. 向量存储
        self.vectorstore = Chroma(
            persist_directory=config.vector_store.persist_directory,
            embedding_function=self.embeddings
        )

        # 3. BM25检索器
        self.bm25_retriever = BM25Retriever.from_documents(
            self._load_documents()
        )

        # 4. 混合检索器
        self.hybrid_retriever = EnsembleRetriever(
            retrievers=[
                self.vectorstore.as_retriever(search_kwargs={"k": 10}),
                self.bm25_retriever
            ],
            weights=[config.retrieval.vector_weight, config.retrieval.keyword_weight]
        )

        # 5. LLM（可切换）
        self.llm = self._create_llm(config)

    def _create_llm(self, config):
        """创建LLM实例，支持多提供商"""
        from langchain_community.chat_models import ChatAnthropic, ChatOpenAI

        if config.llm.provider == "anthropic":
            return ChatAnthropic(
                model=config.llm.model,
                anthropic_api_key=config.llm.api_key
            )
        elif config.llm.provider == "openai":
            return ChatOpenAI(
                model=config.llm.model,
                openai_api_key=config.llm.api_key
            )
        elif config.llm.provider == "deepseek":
            return ChatOpenAI(
                model=config.llm.model,
                openai_api_key=config.llm.api_key,
                openai_api_base="https://api.deepseek.com/v1"
            )

    def retrieve(self, query: str, k: int = 5) -> List[Document]:
        """混合检索"""
        return self.hybrid_retriever.get_relevant_documents(query)[:k]

    def generate_stream(self, query: str, context: str):
        """流式生成"""
        from langchain.prompts import ChatPromptTemplate
        from langchain.schema.output_parser import StrOutputParser
        from langchain.schema.runnable import RunnablePassthrough

        prompt = ChatPromptTemplate.from_template(self._get_prompt_template())
        chain = (
            {"context": RunnablePassthrough(), "query": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.stream({"context": context, "query": query})
```

### 7.3 依赖列表

```txt
# requirements.txt

# Web框架
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0

# LangChain框架
langchain>=0.1.0
langchain-community>=0.0.10
langchain-core>=0.1.0

# Embedding
sentence-transformers>=2.2.0

# 向量数据库
chromadb>=0.4.0

# 关键词检索
rank_bm25>=0.2.2
jieba>=0.42.1

# LLM SDK
anthropic>=0.18.0
openai>=1.0.0

# 工具库
pyyaml>=6.0
python-dotenv>=1.0.0
httpx>=0.24.0

# 测试
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

---

## 八、性能设计

### 8.1 性能目标

| 指标 | 目标值 | 实现策略 |
|------|--------|----------|
| 问答响应时间 | < 3秒 | 异步处理、缓存优化 |
| 检索响应时间 | < 1秒 | 索引优化、批量处理 |
| 并发处理能力 | 100 QPS | 异步API、连接池 |

### 8.2 优化策略

#### 8.2.1 检索优化

```python
# 1. 向量检索优化
- 使用HNSW索引（Chroma默认）
- 预热向量库连接
- 批量查询

# 2. 关键词检索优化
- 预构建BM25索引
- 缓存分词结果
- 倒排索引优化

# 3. 混合检索优化
- LangChain EnsembleRetriever并行执行
- 使用异步IO
```

#### 8.2.2 生成优化

```python
# 1. Prompt优化
- 控制上下文长度
- 缓存常用Prompt模板

# 2. LLM调用优化
- 设置合理的max_tokens
- 使用SSE流式输出提升用户体验
- 实现重试机制

# 3. 流式输出实现
@app.post("/api/v1/qa/stream")
async def qa_stream(request: QARequest):
    async def generate():
        # 先发送元数据
        yield f"event: metadata\ndata: {json.dumps(metadata)}\n\n"

        # 流式发送回答
        async for chunk in llm_service.generate_stream(prompt):
            yield f"event: answer\ndata: {json.dumps({'content': chunk})}\n\n"

        # 发送完成事件
        yield f"event: done\ndata: {json.dumps(stats)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

#### 8.2.3 缓存策略

```python
class CacheStrategy:
    # 1. 查询缓存
    - 缓存相同查询的结果
    - TTL: 1小时

    # 2. Embedding缓存
    - 缓存查询向量
    - 减少重复计算

    # 3. 热点文档缓存
    - 缓存高频访问的chunks
    - 内存缓存
```

---

## 九、日志与监控

### 9.1 日志设计

```python
# 日志格式
{
  "timestamp": "2026-04-30T10:00:00Z",
  "level": "INFO",
  "module": "qa_service",
  "message": "Query processed",
  "extra": {
    "query_id": "abc123",
    "query": "模型训练慢",
    "question_type": "定位指导",
    "response_time_ms": 1234,
    "tokens_used": 1500
  }
}
```

### 9.2 监控指标

```python
# 关键指标
- 请求总数
- 平均响应时间
- 错误率
- LLM token消耗
- 缓存命中率
- 检索召回数量
```

---

## 十、部署设计

### 10.1 开发环境

```bash
# 本地开发
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 构建索引
python scripts/build_index.py

# 启动服务
python src/main.py
```

### 10.2 生产环境（Phase 4）

```yaml
# docker-compose.yaml
version: '3.8'
services:
  ms-rag-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./data:/app/data
```

---

## 十一、测试设计

### 11.1 单元测试

```python
# tests/test_splitter.py
def test_chunk_by_heading():
    """测试按标题切分"""
    pass

def test_chunk_size_limits():
    """测试chunk大小限制"""
    pass

# tests/test_retrieval.py
def test_hybrid_retrieval():
    """测试混合检索"""
    pass

def test_reranking():
    """测试重排序"""
    pass
```

### 11.2 集成测试

```python
# tests/test_qa.py
def test_qa_flow():
    """测试完整问答流程"""
    query = "模型训练慢怎么定位？"
    response = qa_service.answer(query)

    assert response.answer is not None
    assert len(response.sources) > 0
    assert response.question_type in ["定位指导", "问题诊断"]
```

### 11.3 评估测试

```python
# scripts/evaluate.py
def evaluate_retrieval(test_cases: List[TestCase]):
    """评估检索质量"""
    for case in test_cases:
        results = retriever.retrieve(case.query)
        # 计算准确率、召回率
    pass

def evaluate_answer_quality(test_cases: List[TestCase]):
    """评估回答质量"""
    # 使用RAGAS或人工评估
    pass
```

---

## 十二、风险与应对

### 12.1 技术风险

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| 检索效果不佳 | 回答质量下降 | 多种检索策略对比，迭代优化权重 |
| LLM回答不准确 | 用户满意度下降 | Prompt优化，添加回答校验 |
| Embedding模型效果差 | 检索准确率低 | 测试多个模型，选择最优 |

### 12.2 性能风险

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| LLM响应慢 | 用户体验差 | 流式输出、缓存、降级策略 |
| 并发压力大 | 系统不稳定 | 限流、队列、异步处理 |

---

## 十三、实施计划

### 13.1 Phase 1 任务分解

| 任务 | 预计工时 | 优先级 |
|------|----------|--------|
| 项目初始化 | 2h | P0 |
| 文档切分实现 | 4h | P0 |
| 元数据提取实现 | 2h | P0 |
| Embedding服务实现 | 4h | P0 |
| Chroma向量库搭建 | 3h | P0 |
| BM25索引实现 | 3h | P0 |
| 混合检索实现 | 4h | P0 |
| Prompt模板设计 | 2h | P0 |
| LLM服务集成 | 3h | P0 |
| 问答服务实现 | 4h | P0 |
| REST API实现 | 4h | P1 |
| 单元测试 | 4h | P1 |
| 集成测试 | 2h | P1 |

**预计总工时**：约 40 小时（1周）

---

## 十四、附录

### 14.1 问题分类规则

```python
QUESTION_TYPE_RULES = {
    "定位指导": ["怎么定位", "如何定位", "定位方法", "定位流程"],
    "问题诊断": ["是什么原因", "为什么", "怎么办", "如何解决"],
    "工具使用": ["怎么用", "如何使用", "命令", "参数", "工具"],
    "概念理解": ["什么是", "概念", "含义", "定义"],
    "操作步骤": ["如何查看", "怎么操作", "步骤", "界面"]
}
```

### 14.2 关键词词典

```python
KEYWORD_DICT = [
    # 工具类
    "msprof", "msprof-analyze", "MindStudio Insight", "性能采集",

    # 问题类
    "快慢卡", "通信重传", "Host Bound", "下发异常", "算子性能",

    # 概念类
    "AI Core", "AI CPU", "Cube", "MTE", "通算并行",

    # 操作类
    "性能分析", "通信耗时", "算子耗时", "内存分析"
]
```

---

*文档版本：v1.0*
*创建日期：2026-04-30*
