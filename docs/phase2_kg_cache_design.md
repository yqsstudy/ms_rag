# Phase 2 设计文档：知识图谱增强 & 缓存系统

## 一、概述

### 1.1 目标

在 Phase 1 的混合检索（向量 + BM25 + Rerank）基础上，增加两个增强模块：

1. **知识图谱增强（KnowledgeGraph Enhancer）**：利用文档层级关系扩展检索结果，补充上下文
2. **缓存系统（Cache System）**：多级缓存减少重复计算，降低延迟和 LLM 调用成本

### 1.2 设计原则

- 最小侵入：不改变现有检索流程，作为 Rerank 之后的后处理步骤插入
- 可配置：所有参数均可通过 `system.yaml` 调整
- 可降级：缓存未命中或图谱异常时，自动回退到无增强的原始流程

---

## 二、知识图谱增强

### 2.1 核心思路

当前检索返回的 top-K 是孤立的 chunk，缺少文档结构上下文。知识图谱增强通过文档的父子关系和引用关系，在检索后对结果做"上下文补充"。

**数据来源**：不需要额外构建图数据库，直接利用现有元数据：
- `parent_topic` 字段 → 层级边（文档树）
- 文档内容中的 `[title](doc_id)` 超链接 → 引用边
- chunk 的 `keywords` 字段 → 关键词共现边

### 2.2 图结构定义

```python
@dataclass
class GraphNode:
    """图节点，对应一个 chunk"""
    chunk_id: str
    doc_id: str
    doc_title: str
    section_title: str
    content: str
    chunk_type: str  # "parent_overview" | "sibling" | "child" | "reference"

@dataclass
class GraphEdge:
    """图边"""
    source_id: str
    target_id: str
    edge_type: str  # "parent" | "child" | "sibling" | "reference" | "keyword_cooccur"
    weight: float   # 0.0 - 1.0

class DocumentGraph:
    """文档关系图"""
    nodes: Dict[str, GraphNode]       # chunk_id → GraphNode
    edges: Dict[str, List[GraphEdge]] # doc_id → edges

    # 索引结构
    parent_map: Dict[str, str]        # doc_id → parent_doc_id
    children_map: Dict[str, List[str]] # doc_id → [child_doc_ids]
    doc_chunks_map: Dict[str, List[str]] # doc_id → [chunk_ids]
```

### 2.3 图的构建（离线）

在 `build_index.py` 构建向量索引的同时，生成 `data/graph.json`。

**构建流程**：

```
遍历所有文档元数据
    │
    ├── 1. 解析 parent_topic → 建立 parent_map / children_map
    │
    ├── 2. 解析文档内容中的 [title](doc_id) 链接 → 建立 reference 边
    │
    ├── 3. 按 doc_id 聚合 chunk_ids → 建立 doc_chunks_map
    │
    └── 4. 序列化为 JSON 持久化
```

**JSON 格式**：

```json
{
  "parent_map": {
    "toolsample6_005": "toolsample6_002",
    "toolsample6_006": "toolsample6_005"
  },
  "children_map": {
    "toolsample6_001": ["toolsample6_002", "toolsample6_003"],
    "toolsample6_002": ["toolsample6_005", "toolsample6_007"]
  },
  "doc_chunks_map": {
    "toolsample6_005": ["toolsample6_005_chunk_0", "toolsample6_005_chunk_1"]
  },
  "references": {
    "toolsample6_006": ["toolsample6_005", "toolsample6_009"]
  }
}
```

### 2.4 图的使用（在线增强）

**插入位置**：在 `Reranker.rerank()` 之后、送入 `ContextBuilder` 之前。

```
HybridRetriever.retrieve()
    │
    ▼
Reranker.rerank()
    │
    ▼
KnowledgeGraphEnhancer.enhance()  ← 新增步骤
    │
    ▼
ContextBuilder.build_context()
```

**增强策略**：

```python
class KnowledgeGraphEnhancer:
    def enhance(
        self,
        results: List[HybridResult],
        query: str,
    ) -> List[HybridResult]:
        """
        对检索结果做图增强，返回扩展后的结果列表。

        流程：
        1. 收集原始结果中的 doc_id 集合
        2. 对每个结果做三向扩展
        3. 去重（同一 doc_id 只保留最高分的 chunk）
        4. 扩展结果降权后插入
        5. 截断到 max_enhanced_results
        """
```

**三向扩展规则**：

| 扩展方向 | 规则 | 取哪个 chunk | 扩展权重 |
|---------|------|-------------|---------|
| 向上 | 父文档存在 | 父文档的第一个 chunk（通常是概述） | 0.5 |
| 横向 | 兄弟文档存在 | 每个兄弟文档的第一个 chunk | 0.3 |
| 向下 | 子文档存在 | 子文档的标题级 chunk（section_title 含关键词） | 0.3 |
| 引用 | 文档中有超链接指向其他文档 | 被引用文档的第一个 chunk | 0.4 |

**去重策略**：
- 同一 `chunk_id` 出现在原始结果和扩展结果中 → 保留原始分数
- 同一 `doc_id` 的多个扩展 chunk → 只保留分数最高的一个
- 扩展结果总数不超过 `max_enhanced_results`（默认 3）

**扩展结果的排序**：
- 扩展 chunk 以 `原始最高分 × 扩展权重` 插入到结果列表
- 保持原始结果的相对顺序不变，扩展 chunk 插入到对应位置

### 2.5 关联推荐

在 LLM 回答之后，从图中提取关联主题作为"相关推荐"返回给前端。

```python
def get_related_topics(
    self,
    results: List[HybridResult],
) -> List[dict]:
    """
    基于当前结果的 doc_id，返回关联主题列表。

    返回格式：
    [
        {"title": "通信重传解决方案", "doc_id": "toolsample6_006", "relation": "child"},
        {"title": "性能定位流程", "doc_id": "toolsample6_002", "relation": "parent"},
    ]
    """
```

**推荐规则**：
- 从原始 top-K 结果的 doc_id 出发
- 收集父文档、子文档、兄弟文档、引用文档的标题
- 排除已在 sources 中出现的文档
- 按 relation 类型排序：parent > child > sibling > reference
- 最多返回 5 个推荐

### 2.6 配置项

```yaml
# config/system.yaml
knowledge_graph:
  enabled: true
  graph_path: "./data/graph.json"
  expand_parent: true          # 向上扩展
  expand_sibling: true         # 横向扩展
  expand_child: true           # 向下扩展
  expand_reference: true       # 引用扩展
  max_expand_per_direction: 1  # 每个方向最多扩展几个
  max_enhanced_results: 3      # 扩展结果总数上限
  expand_weight_parent: 0.5    # 父文档扩展权重
  expand_weight_sibling: 0.3   # 兄弟文档扩展权重
  expand_weight_child: 0.3     # 子文档扩展权重
  expand_weight_reference: 0.4 # 引用扩展权重
  related_topics_count: 5      # 关联推荐数量
```

### 2.7 对现有代码的改动

| 文件 | 改动内容 |
|------|---------|
| `src/retrieval/kg_enhancer.py` | **新增**：知识图谱增强器 |
| `scripts/build_index.py` | **修改**：构建索引时同步生成 `graph.json` |
| `src/pipeline/rag_pipeline.py` | **修改**：在 rerank 后调用 `kg_enhancer.enhance()` |
| `src/generation/context_builder.py` | **修改**：支持接收扩展结果并区分来源 |
| `src/api/routes.py` | **修改**：SSE metadata 事件中增加 `related_topics` 字段 |
| `config/system.yaml` | **修改**：增加 `knowledge_graph` 配置段 |
| `src/core/config.py` | **修改**：增加 `KnowledgeGraphConfig` 数据类 |

### 2.8 前端改动

| 文件 | 改动内容 |
|------|---------|
| `frontend/src/types/index.ts` | `SSEMetadata` 增加 `related_topics` 字段 |
| `frontend/src/components/MessageCard.vue` | AI 回答下方增加"相关主题"推荐区域 |
| `frontend/src/components/RelatedTopics.vue` | **新增**：相关主题组件 |

**RelatedTopics 组件交互**：
- 显示 3-5 个相关主题按钮
- 点击后自动将该主题作为新问题发送
- 样式参考搜索引擎的"相关搜索"

---

## 三、缓存系统

### 3.1 三级缓存架构

```
请求进入
    │
    ▼
L1: 精确匹配缓存 ──命中──▶ 直接返回完整响应
    │未命中
    ▼
L2: 语义相似缓存 ──命中──▶ 直接返回完整响应
    │未命中
    ▼
L3: Embedding 缓存 ──命中──▶ 跳过 embedding，进入检索
    │未命中
    ▼
完整 RAG 链路（embedding → 检索 → rerank → KG增强 → LLM生成）
    │
    ▼
结果写入 L1 + L3 缓存
```

### 3.2 L1：精确匹配缓存

**用途**：完全相同的问题直接返回缓存结果。

**实现**：

```python
class ExactCache:
    """基于 query hash 的精确匹配缓存"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.ttl = ttl_seconds

    def get(self, query: str) -> Optional[CacheEntry]:
        key = self._make_key(query)
        entry = self.cache.get(key)
        if entry and not entry.is_expired():
            entry.hit_count += 1
            return entry
        if entry:
            del self.cache[key]  # 过期删除
        return None

    def put(self, query: str, response: dict, metadata: dict):
        key = self._make_key(query)
        # LRU 淘汰：超过 max_size 时删除最旧的
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = CacheEntry(
            key=key,
            response=response,
            metadata=metadata,
            created_at=time.time(),
            ttl=self.ttl,
        )

    def _make_key(self, query: str) -> str:
        """query 归一化后取 hash"""
        normalized = query.strip().lower()
        return hashlib.md5(normalized.encode()).hexdigest()

    def invalidate_by_doc(self, doc_id: str):
        """文档更新时清除包含该文档来源的缓存"""
        keys_to_remove = []
        for key, entry in self.cache.items():
            source_doc_ids = [s["doc_id"] for s in entry.response.get("sources", [])]
            if doc_id in source_doc_ids:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.cache[key]
```

**CacheEntry 结构**：

```python
@dataclass
class CacheEntry:
    key: str
    response: dict          # 完整的 QAResponse 序列化
    metadata: dict          # 额外元信息（命中文档列表等）
    created_at: float
    ttl: int
    hit_count: int = 0

    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl
```

**缓存内容**：

```json
{
  "answer": "针对模型训练速度慢的问题...",
  "sources": [...],
  "question_type": "定位指导",
  "keywords": ["训练", "定位"],
  "metadata": {
    "model": "claude-sonnet-4-6",
    "cached": true,
    "cache_level": "L1"
  }
}
```

**query 归一化规则**：
1. 去除首尾空白
2. 转小写
3. 全角转半角
4. 去除标点符号
5. 去除多余空格

### 3.3 L2：语义相似缓存

**用途**：措辞不同但语义相同的问题返回缓存结果。

**实现方案**：维护一个最近查询的向量索引，在缓存层做一次轻量向量搜索。

```python
class SemanticCache:
    """基于向量相似度的语义缓存"""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        max_size: int = 500,
        ttl_seconds: int = 1800,
        similarity_threshold: float = 0.92,
    ):
        self.embedding_service = embedding_service
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.threshold = similarity_threshold

        # 内存中的向量索引
        self.vectors: Dict[str, np.ndarray] = {}   # key → embedding
        self.entries: Dict[str, CacheEntry] = {}    # key → CacheEntry

    def get(self, query: str, query_embedding: List[float]) -> Optional[CacheEntry]:
        """查找语义相似的缓存"""
        if not self.vectors:
            return None

        # 计算与所有缓存向量的余弦相似度
        best_score = 0.0
        best_key = None

        query_vec = np.array(query_embedding)
        for key, vec in self.vectors.items():
            score = np.dot(query_vec, vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(vec) + 1e-8
            )
            if score > best_score:
                best_score = score
                best_key = key

        if best_score >= self.threshold and best_key in self.entries:
            entry = self.entries[best_key]
            if not entry.is_expired():
                entry.hit_count += 1
                return entry
            else:
                self._remove(best_key)

        return None

    def put(self, query: str, query_embedding: List[float], response: dict):
        key = hashlib.md5(query.strip().lower().encode()).hexdigest()
        if len(self.entries) >= self.max_size:
            self._evict_oldest()
        self.vectors[key] = np.array(query_embedding)
        self.entries[key] = CacheEntry(
            key=key,
            response=response,
            metadata={"original_query": query},
            created_at=time.time(),
            ttl=self.ttl,
        )
```

**阈值选择**：

| 阈值 | 含义 | 预期效果 |
|------|------|---------|
| 0.95 | 几乎完全相同 | 精准但命中率低，"训练慢" vs "训练很慢" 可能 miss |
| 0.92 | 高度相似 | 推荐选择，平衡精准和命中率 |
| 0.85 | 较为相似 | 命中率高但可能误匹配，"通信慢" vs "通信重传" |

**向量复用**：L2 缓存的 query_embedding 来自 L3 缓存或实时计算，不需要额外的 embedding 调用。在完整链路中，embedding 计算一次，同时写入 L3 和 L2。

**淘汰策略**：
- TTL 过期自动删除
- 超过 max_size 时按 `created_at` 淘汰最旧的
- 支持按 doc_id 精准失效

### 3.4 L3：Embedding 缓存

**用途**：缓存 query → embedding 映射，跳过重复的 embedding 计算。

**实现**：

```python
class EmbeddingCache:
    """Embedding 向量缓存"""

    def __init__(self, max_size: int = 2000, ttl_seconds: int = 7200):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.ttl = ttl_seconds

    def get(self, query: str) -> Optional[List[float]]:
        key = self._make_key(query)
        entry = self.cache.get(key)
        if entry and not entry.is_expired():
            return entry.response  # response 存的就是 embedding vector
        if entry:
            del self.cache[key]
        return None

    def put(self, query: str, embedding: List[float]):
        key = self._make_key(query)
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = CacheEntry(
            key=key,
            response=embedding,
            metadata={},
            created_at=time.time(),
            ttl=self.ttl,
        )

    def _make_key(self, query: str) -> str:
        normalized = query.strip().lower()
        return hashlib.md5(normalized.encode()).hexdigest()
```

### 3.5 缓存管理器

统一管理三级缓存，对外提供简洁接口。

```python
class CacheManager:
    """多级缓存管理器"""

    def __init__(self, settings: CacheConfig, embedding_service: EmbeddingService):
        self.enabled = settings.enabled
        self.l1 = ExactCache(
            max_size=settings.l1_max_size,
            ttl_seconds=settings.l1_ttl,
        )
        self.l2 = SemanticCache(
            embedding_service=embedding_service,
            max_size=settings.l2_max_size,
            ttl_seconds=settings.l2_ttl,
            similarity_threshold=settings.l2_threshold,
        )
        self.l3 = EmbeddingCache(
            max_size=settings.l3_max_size,
            ttl_seconds=settings.l3_ttl,
        )

        # 统计
        self.stats = CacheStats()

    def get(self, query: str) -> Optional[dict]:
        """尝试从缓存获取完整响应"""
        if not self.enabled:
            return None

        # L1: 精确匹配
        entry = self.l1.get(query)
        if entry:
            self.stats.l1_hits += 1
            response = entry.response.copy()
            response["metadata"]["cache_level"] = "L1"
            response["metadata"]["cached"] = True
            return response
        self.stats.l1_misses += 1

        # L2: 语义相似（需要 embedding）
        # 注意：L2 的 get 需要 query_embedding，由调用方传入
        return None

    def get_with_embedding(
        self, query: str, query_embedding: List[float]
    ) -> Optional[dict]:
        """带 embedding 的缓存查找（L1 + L2）"""
        # L1
        result = self.get(query)
        if result:
            return result

        # L2
        entry = self.l2.get(query, query_embedding)
        if entry:
            self.stats.l2_hits += 1
            response = entry.response.copy()
            response["metadata"]["cache_level"] = "L2"
            response["metadata"]["cached"] = True
            return response
        self.stats.l2_misses += 1

        return None

    def get_embedding(self, query: str) -> Optional[List[float]]:
        """从 L3 获取缓存的 embedding"""
        embedding = self.l3.get(query)
        if embedding:
            self.stats.l3_hits += 1
        else:
            self.stats.l3_misses += 1
        return embedding

    def put(self, query: str, query_embedding: List[float], response: dict):
        """将结果写入所有缓存层"""
        self.l1.put(query, response, {})
        self.l2.put(query, query_embedding, response)
        self.l3.put(query, query_embedding)

    def invalidate_by_doc(self, doc_id: str):
        """文档更新时失效相关缓存"""
        self.l1.invalidate_by_doc(doc_id)
        self.l2.invalidate_by_doc(doc_id)
        # L3 是 embedding 缓存，不依赖文档内容，无需失效

    def get_stats(self) -> dict:
        return {
            "l1_hit_rate": self.stats.l1_hit_rate,
            "l2_hit_rate": self.stats.l2_hit_rate,
            "l3_hit_rate": self.stats.l3_hit_rate,
            "total_requests": self.stats.total_requests,
        }


@dataclass
class CacheStats:
    l1_hits: int = 0
    l1_misses: int = 0
    l2_hits: int = 0
    l2_misses: int = 0
    l3_hits: int = 0
    l3_misses: int = 0

    @property
    def total_requests(self) -> int:
        return self.l1_hits + self.l1_misses

    @property
    def l1_hit_rate(self) -> float:
        total = self.l1_hits + self.l1_misses
        return self.l1_hits / total if total > 0 else 0.0

    @property
    def l2_hit_rate(self) -> float:
        total = self.l2_hits + self.l2_misses
        return self.l2_hits / total if total > 0 else 0.0

    @property
    def l3_hit_rate(self) -> float:
        total = self.l3_hits + self.l3_misses
        return self.l3_hits / total if total > 0 else 0.0
```

### 3.6 流式响应缓存

SSE 流式响应需要特殊处理：先收集完整响应，再写入缓存。

```python
# 在 RAGPipeline.query_stream() 中的处理逻辑

def query_stream_with_cache(self, question: str, top_k: int = 5):
    # 1. 尝试缓存
    cached = self.cache_manager.get(question)
    if cached:
        # 从缓存的完整文本构造伪 stream
        return self._make_cached_stream(cached)

    # 2. 正常 RAG 链路
    metadata, stream, meta = self._query_stream_internal(question, top_k)

    # 3. 包装 stream，收集完整响应后写入缓存
    def caching_stream():
        full_answer = ""
        for chunk in stream:
            full_answer += chunk
            yield chunk
        # 流结束后写入缓存
        response = {
            "answer": full_answer,
            "sources": metadata.get("sources", []),
            "question_type": metadata.get("question_type", ""),
            "keywords": metadata.get("keywords", []),
            "metadata": meta,
        }
        self.cache_manager.put(question, query_embedding, response)

    return metadata, caching_stream(), meta


def _make_cached_stream(self, cached: dict):
    """将缓存的完整文本转为 SSE 事件流"""
    answer = cached["answer"]
    # 按句子/段落分块模拟流式输出
    chunks = self._split_for_streaming(answer)

    def fake_stream():
        for chunk in chunks:
            yield chunk

    metadata = {
        "question_type": cached.get("question_type", ""),
        "keywords": cached.get("keywords", []),
        "sources": cached.get("sources", []),
        "cached": True,
    }
    return metadata, fake_stream(), cached.get("metadata", {})
```

### 3.7 缓存失效

**触发条件**：

| 事件 | 失效策略 |
|------|---------|
| 文档更新（`build_index.py` 重新执行） | 清除所有缓存 |
| 单篇文档删除 | 按 doc_id 精准失效 L1/L2 |
| 缓存 TTL 过期 | 自动过期，惰性删除 |
| 手动清缓存 API | 清除所有缓存 |

**清缓存 API**：

```http
POST /api/v1/cache/clear
Content-Type: application/json

{
  "level": "all"  // "all" | "l1" | "l2" | "l3"
}
```

### 3.8 配置项

```yaml
# config/system.yaml
cache:
  enabled: true
  l1:
    max_size: 1000        # 最大缓存条目数
    ttl: 3600             # 过期时间（秒）
  l2:
    max_size: 500
    ttl: 1800
    threshold: 0.92       # 语义相似度阈值
  l3:
    max_size: 2000
    ttl: 7200
```

### 3.9 对现有代码的改动

| 文件 | 改动内容 |
|------|---------|
| `src/cache/cache_manager.py` | **新增**：缓存管理器 |
| `src/cache/exact_cache.py` | **新增**：L1 精确缓存 |
| `src/cache/semantic_cache.py` | **新增**：L2 语义缓存 |
| `src/cache/embedding_cache.py` | **新增**：L3 Embedding 缓存 |
| `src/pipeline/rag_pipeline.py` | **修改**：在 query/query_stream 开头查缓存，结尾写缓存 |
| `src/api/routes.py` | **修改**：增加 `/api/v1/cache/clear` 端点；SSE metadata 增加 `cached` 字段 |
| `config/system.yaml` | **修改**：增加 `cache` 配置段 |
| `src/core/config.py` | **修改**：增加 `CacheConfig` 数据类 |

### 3.10 前端改动

| 文件 | 改动内容 |
|------|---------|
| `frontend/src/types/index.ts` | `SSEMetadata` 增加 `cached: boolean` 字段 |
| `frontend/src/components/MessageCard.vue` | 响应时间旁显示"缓存命中"标识 |

---

## 四、集成：RAGPipeline 改造

改造后的 `query_stream()` 完整流程：

```
query_stream(question, top_k)
    │
    ├── 0. CacheManager.get(question)  ← L1 精确匹配
    │   └── 命中 → 返回 _make_cached_stream()
    │
    ├── 1. EmbeddingService.embed_query(question)
    │   ├── CacheManager.get_embedding()  ← L3 命中则跳过
    │   └── 未命中 → 计算 embedding，写入 L3
    │
    ├── 2. CacheManager.get_with_embedding()  ← L2 语义匹配
    │   └── 命中 → 返回 _make_cached_stream()
    │
    ├── 3. HybridRetriever.retrieve()
    ├── 4. Reranker.rerank()
    ├── 5. KnowledgeGraphEnhancer.enhance()  ← 新增
    ├── 6. ContextBuilder.build_context()
    ├── 7. PromptTemplateManager.render()
    ├── 8. LLMService.generate_stream()
    │
    └── 9. CacheManager.put()  ← 流结束后写入 L1 + L2 + L3
```

**关键改造点**：

```python
class RAGPipeline:
    def __init__(self, settings: Settings):
        # ... 现有初始化 ...

        # 新增组件
        self.kg_enhancer = KnowledgeGraphEnhancer(
            graph_path=settings.knowledge_graph.graph_path,
            config=settings.knowledge_graph,
            vector_store=self.vector_store,
        )
        self.cache_manager = CacheManager(
            settings=settings.cache,
            embedding_service=self.embedding_service,
        )

    def query_stream(self, question: str, top_k: int = 5):
        # L1 缓存
        cached = self.cache_manager.get(question)
        if cached:
            return self._make_cached_stream(cached)

        # Embedding（带 L3 缓存）
        cached_embedding = self.cache_manager.get_embedding(question)
        if cached_embedding:
            query_embedding = cached_embedding
        else:
            query_embedding = self.embedding_service.embed_query(question)
            self.cache_manager.put_embedding(question, query_embedding)

        # L2 缓存
        cached = self.cache_manager.get_with_embedding(question, query_embedding)
        if cached:
            return self._make_cached_stream(cached)

        # 正常 RAG 链路
        results = self.retriever.retrieve(question, query_embedding, k=top_k * 2)
        if self.settings.retrieval.rerank:
            results = self.reranker.rerank(results)

        # 知识图谱增强
        results = self.kg_enhancer.enhance(results, question)
        results = results[:top_k]

        question_type = self._classify_question(question)
        context = self.context_builder.build_context(results)
        prompt = self.prompt_manager.render(question_type, question, context)

        # 关联推荐
        related_topics = self.kg_enhancer.get_related_topics(results)

        metadata = {
            "question_type": question_type,
            "keywords": self._extract_keywords(question),
            "sources": self.context_builder.build_sources(results),
            "related_topics": related_topics,
        }

        llm = self._get_llm_service()
        stream = llm.generate_stream(prompt)

        # 包装 stream 以收集缓存
        def caching_stream():
            full_answer = ""
            for chunk in stream:
                full_answer += chunk
                yield chunk
            self.cache_manager.put(question, query_embedding, {
                "answer": full_answer,
                "sources": metadata["sources"],
                "question_type": question_type,
                "keywords": metadata["keywords"],
            })

        return metadata, caching_stream(), {"model": self.settings.llm.model}
```

---

## 五、监控与日志

### 5.1 缓存监控指标

```python
# 每次请求记录
logger.info(f"[Cache] L1={'HIT' if l1_hit else 'MISS'} L2={'HIT' if l2_hit else 'MISS'} L3={'HIT' if l3_hit else 'MISS'}")

# 定期记录统计（每 100 次请求）
logger.info(f"[Cache Stats] L1 hit rate: {l1_rate:.1%}, L2 hit rate: {l2_rate:.1%}, L3 hit rate: {l3_rate:.1%}")
```

### 5.2 图谱增强监控

```python
logger.info(f"[KG] Original: {len(original)} results, Enhanced: {len(enhanced)} results")
logger.info(f"[KG] Related topics: {len(related_topics)}")
```

---

## 六、文件结构

```
src/
├── cache/                          # 新增目录
│   ├── __init__.py
│   ├── cache_manager.py            # 缓存管理器
│   ├── exact_cache.py              # L1 精确缓存
│   ├── semantic_cache.py           # L2 语义缓存
│   └── embedding_cache.py          # L3 Embedding 缓存
│
├── retrieval/
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   └── kg_enhancer.py              # 新增：知识图谱增强器
│
└── core/
    └── config.py                   # 新增 CacheConfig, KnowledgeGraphConfig

config/
└── system.yaml                     # 新增 cache, knowledge_graph 配置段

data/
└── graph.json                      # 构建索引时生成的文档关系图

scripts/
└── build_index.py                  # 修改：增加 graph.json 生成逻辑

frontend/src/
├── components/
│   ├── RelatedTopics.vue           # 新增：相关主题推荐组件
│   └── MessageCard.vue             # 修改：增加缓存标识和相关主题区域
└── types/
    └── index.ts                    # 修改：SSEMetadata 增加字段
```

---

## 七、实施顺序

| 步骤 | 内容 | 预计工时 |
|------|------|---------|
| 1 | `CacheConfig` / `KnowledgeGraphConfig` 数据类 + system.yaml 配置 | 0.5h |
| 2 | L1 `ExactCache` 实现 | 1h |
| 3 | L3 `EmbeddingCache` 实现 | 0.5h |
| 4 | `CacheManager` 集成三级缓存 | 1h |
| 5 | `RAGPipeline` 接入缓存（query + query_stream） | 1.5h |
| 6 | L2 `SemanticCache` 实现 | 1.5h |
| 7 | `DocumentGraph` 构建逻辑（build_index.py） | 1h |
| 8 | `KnowledgeGraphEnhancer` 三向扩展 + 关联推荐 | 2h |
| 9 | `RAGPipeline` 接入图谱增强 | 0.5h |
| 10 | API 路由改动（cache clear 端点、metadata 字段） | 0.5h |
| 11 | 前端：RelatedTopics 组件 + 缓存标识 | 1.5h |
| 12 | 集成测试 + 日志验证 | 1h |
| **合计** | | **~12h** |

---

## 八、风险与降级

| 风险 | 影响 | 降级方案 |
|------|------|---------|
| graph.json 缺失 | KG 增强不可用 | `KnowledgeGraphEnhancer` 检测文件不存在时直接 passthrough |
| L2 语义缓存误匹配 | 返回不相关回答 | 阈值设为 0.92 兜底；前端显示"缓存命中"让用户可感知 |
| 缓存内存占用过高 | OOM | max_size 上限 + TTL 过期淘汰；监控内存使用 |
| 文档更新后缓存不一致 | 回答过时 | build_index.py 执行后自动调用 cache clear all |

---

## 九、当前代码落地状态

截至 2026-05-21，代码已落地本设计中的主要能力：`src/cache/` 实现 L1/L2/L3 缓存，`src/retrieval/kg_enhancer.py` 实现知识图谱增强，`scripts/build_index.py` 构建 `data/graph.json` 和 `data/docstore/`，`src/api/routes.py` 暴露缓存统计与清理接口，前端通过 `RelatedTopics.vue` 展示相关主题。当前 `config/system.yaml` 使用扁平字段配置缓存，例如 `l1_max_size`、`l1_ttl`、`l2_threshold`，而不是本文早期示例中的嵌套 `l1/l2/l3` 结构。

*文档版本：v1.1*
*创建日期：2026-05-04*
*更新日期：2026-05-21*
