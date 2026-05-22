# RAG 评测集生成与指标验证脚本需求规格

## 1. 背景

当前 `ms_rag` 已具备领域文档知识库、RAG Pipeline、混合检索、缓存和评测脚本基础，但用于验证系统效果的评测数据集不足。为了更客观地评估检索与生成质量，需要设计一套可离线执行的评测集生成与指标验证脚本。

该脚本的目标不是替代线上 RAG 主链路，而是用于离线构建弱监督评测集、生成少量人工审核黄金集、对比不同 RAG 配置，并为 chunk 策略、检索权重、rerank 参数和 prompt 优化提供依据。

## 2. 目标

### 2.1 核心目标

- 基于现有 `corpus/` 文档自动生成 RAG 评测样本。
- 支持每一步单独执行，便于调试、复用和失败恢复。
- 支持 OpenAI-compatible API 配置，用于问题生成、证据筛选、答案要点归纳和 LLM-as-Judge。
- 构建多证据支持的评测样本，避免单一 chunk 标准答案导致的误判。
- 降低使用被测 RAG 系统构造评测集带来的自举偏置。
- 输出可用于检索指标、生成指标和端到端指标评估的数据文件。

### 2.2 非目标

- 不要求实现在线 RAG 深度问答链路。
- 不要求替代现有 `RAGPipeline`。
- 不要求一次性构建大规模人工标注数据集。
- 不要求引入新的专有评测平台。
- 不要求所有评测样本完全人工审核。

## 3. 用户故事

### 3.1 自动生成评测问题

作为开发者，我希望可以从知识库 chunk 中自动生成候选问题，以便快速获得覆盖不同文档和主题的评测样本。

验收标准：

- 可以指定输入文档目录或 chunk 文件。
- 可以指定每个 chunk 生成的问题数量。
- 生成问题包含 `question_type`、`difficulty`、`keywords` 等字段。
- 生成结果可保存为中间文件，后续步骤可重复使用。

### 3.2 构建高召回候选证据池

作为开发者，我希望对每个候选问题构建较高召回的候选证据池，而不是只依赖当前线上 RAG top-k，以降低评测集偏置。

验收标准：

- 候选证据池至少支持以下来源：
  - seed chunk；
  - seed chunk 前后邻近 chunk；
  - seed chunk 所在文档或 section；
  - BM25 高召回结果；
  - 向量检索高召回结果；
  - 标题或关键词匹配结果。
- 支持配置各路候选数量，例如 `bm25_top_k`、`vector_top_k`、`neighbor_window`。
- 候选证据池需要去重。
- 候选证据池生成结果可保存为中间文件。

### 3.3 机器粗筛与 Evidence Card 压缩

作为开发者，我希望在调用 LLM 前先用规则和分数做粗筛，并将 chunk 压缩为 evidence card，以控制 LLM 输入规模和成本。

验收标准：

- 支持按 BM25 分数、向量分数、标题匹配、同文档加权、seed 邻近关系进行综合排序。
- 支持限制每个问题进入 LLM 判断的候选数量，例如 20-30 个。
- evidence card 至少包含：
  - `chunk_id`；
  - `source_file`；
  - `title` 或 `section_path`；
  - `matched_keywords`；
  - `snippet`；
  - `bm25_rank`；
  - `vector_rank`。
- evidence card 的 snippet 长度可配置。

### 3.4 LLM 证据相关性判断

作为开发者，我希望 LLM 只负责判断候选 evidence card 是否支持回答问题，而不是一次性完成所有任务。

验收标准：

- LLM 对每个候选 chunk 输出相关性等级：
  - `0`: 无关；
  - `1`: 主题相关但不能回答；
  - `2`: 部分支持；
  - `3`: 直接支持。
- 保留 `relevance >= 2` 的 chunk 作为 supporting evidence 候选。
- 输出每个相关 chunk 支持的要点和简短原因。
- 支持失败重试和 JSON 解析失败处理。
- 支持将判断结果保存为中间文件。

### 3.5 答案要点归纳

作为开发者，我希望基于筛选后的少量 supporting chunks，让 LLM 合并答案要点并生成标准评测结构。

验收标准：

- 输入为问题和筛选后的 supporting chunk 原文。
- 输出包含：
  - `answer_key_points`；
  - `must_have_points`；
  - `nice_to_have_points`；
  - `expected_answer`；
  - `acceptable_chunk_ids`；
  - `acceptable_source_files`；
  - `conflicts`；
  - `is_answerable`。
- 每个答案要点需要尽量绑定 supporting chunk。
- 如果候选证据不足以回答问题，应输出 `is_answerable=false`。
- 输出可保存为最终评测集草稿。

### 3.6 人工审核抽样集

作为开发者，我希望可以导出一部分样本用于人工审核，防止自动生成的评测集过度偏置或质量不稳定。

验收标准：

- 支持按 `question_type`、`difficulty`、source 分层抽样。
- 支持导出 Markdown 或 JSONL 格式审核文件。
- 审核字段应包含问题、标准答案、must-have points、supporting chunks 和原文片段。
- 支持人工审核结果回填，例如 `approved`、`rejected`、`needs_edit`。

### 3.7 固定评测集并运行系统评估

作为开发者，我希望可以基于固定的评测集运行 RAG 系统指标验证，并比较不同配置的效果。

验收标准：

- 支持读取固定 `eval_dataset.jsonl`。
- 支持运行当前 RAG Pipeline 得到检索结果和生成答案。
- 支持计算检索指标：
  - Evidence Hit@K；
  - Evidence Recall@K；
  - MRR；
  - NDCG@K。
- 支持计算生成指标：
  - must-have coverage；
  - nice-to-have coverage；
  - keyword coverage；
  - LLM-as-Judge correctness；
  - LLM-as-Judge faithfulness；
  - LLM-as-Judge completeness；
  - LLM-as-Judge relevance。
- 支持记录 latency。
- 支持按 `question_type`、`difficulty`、source 分组统计。
- 支持导出 JSON 和 Markdown 报告。

## 4. 分步执行要求

脚本必须支持每一步单独执行。推荐提供一个统一 CLI，例如：

```bash
python scripts/rag_eval_dataset.py generate-questions --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py build-evidence-pool --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py build-evidence-cards --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py judge-evidence --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py synthesize-answers --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py export-review-set --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py evaluate --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py report --config config/rag_eval.yaml
```

也可以拆分为多个脚本，但必须满足：

- 每一步有明确输入文件；
- 每一步有明确输出文件；
- 每一步可重复执行；
- 每一步失败后可以从中间产物恢复；
- 每一步支持 `--limit` 便于小样本调试；
- 每一步支持 `--dry-run` 或等价调试模式。

## 5. OpenAI-compatible API 配置要求

脚本应支持 OpenAI-compatible Chat Completions API。配置项建议包括：

```yaml
llm:
  provider: openai_compatible
  base_url: "${OPENAI_BASE_URL}"
  api_key: "${OPENAI_API_KEY}"
  model: "${OPENAI_MODEL:gpt-4o-mini}"
  temperature: 0.2
  max_tokens: 4096
  timeout_seconds: 60
  max_retries: 3
  retry_backoff_seconds: 2
```

要求：

- 支持环境变量注入。
- 支持自定义 `base_url`。
- 支持自定义模型名。
- 支持请求超时。
- 支持失败重试。
- 不允许将 API Key 写入输出日志。
- LLM 原始响应和解析后 JSON 可选保存，便于调试。

## 6. 数据格式要求

### 6.1 候选问题文件

示例：

```json
{
  "id": "q_000001",
  "question": "如何定位通信耗时过高的问题？",
  "seed_chunk_id": "chunk_101",
  "seed_source_file": "corpus/xxx.md",
  "question_type": "troubleshooting",
  "difficulty": "medium",
  "keywords": ["通信耗时", "rank", "trace"]
}
```

### 6.2 候选证据池文件

示例：

```json
{
  "question_id": "q_000001",
  "candidate_chunks": [
    {
      "chunk_id": "chunk_101",
      "source_file": "corpus/xxx.md",
      "origin": ["seed", "bm25"],
      "bm25_score": 12.3,
      "vector_score": 0.82
    }
  ]
}
```

### 6.3 Evidence Card 文件

示例：

```json
{
  "question_id": "q_000001",
  "cards": [
    {
      "chunk_id": "chunk_101",
      "source_file": "corpus/xxx.md",
      "title": "通信耗时分析",
      "section_path": "性能分析 > 通信分析",
      "matched_keywords": ["通信耗时", "rank"],
      "snippet": "通信耗时分析可以通过 trace 中的通信算子耗时和 rank 间差异进行定位...",
      "bm25_rank": 3,
      "vector_rank": 7
    }
  ]
}
```

### 6.4 最终评测集文件

示例：

```json
{
  "id": "eval_000001",
  "question": "如何定位通信耗时过高的问题？",
  "question_type": "troubleshooting",
  "difficulty": "medium",
  "answer_key_points": [
    {
      "point": "采集 trace 数据",
      "supporting_chunks": ["chunk_045"]
    },
    {
      "point": "分析通信算子或通信阶段的耗时占比",
      "supporting_chunks": ["chunk_101"]
    }
  ],
  "must_have_points": [
    "采集 trace 数据",
    "分析通信耗时",
    "对比 rank 或 iteration"
  ],
  "nice_to_have_points": [
    "结合 Timeline 查看通信等待",
    "检查是否存在慢 rank"
  ],
  "expected_answer": "可以先采集 trace 数据，再查看通信算子或通信阶段的耗时占比，并对比不同 rank 或 iteration 的耗时差异来定位是否存在慢 rank、通信等待或负载不均衡。",
  "acceptable_chunk_ids": ["chunk_045", "chunk_101", "chunk_238"],
  "acceptable_source_files": ["trace_collection.md", "communication_analysis.md", "rank_analysis.md"],
  "keywords": ["通信耗时", "trace", "rank", "Timeline"],
  "is_answerable": true
}
```

## 7. 指标要求

### 7.1 检索指标

- Evidence Hit@K：top-k 是否命中任意 `acceptable_chunk_ids`。
- Evidence Recall@K：top-k 命中的 acceptable chunks 数量 / acceptable chunks 总数量。
- MRR：第一个 acceptable chunk 的倒数排名。
- NDCG@K：基于 evidence relevance 计算排序质量。

### 7.2 生成指标

- Must-have Coverage：模型回答覆盖的必答点比例。
- Nice-to-have Coverage：模型回答覆盖的加分点比例。
- Keyword Coverage：模型回答覆盖的关键词比例。
- LLM-as-Judge Correctness：答案正确性评分。
- LLM-as-Judge Faithfulness：答案是否忠于检索上下文。
- LLM-as-Judge Completeness：答案完整性评分。
- LLM-as-Judge Relevance：答案是否切题。

### 7.3 性能指标

- 平均检索耗时。
- 平均生成耗时。
- 端到端平均耗时。
- P50 / P95 latency。
- LLM 调用次数。
- token 消耗估算。

## 8. 配置要求

推荐配置文件：`config/rag_eval.yaml`。

配置内容应至少包括：

```yaml
paths:
  corpus_dir: "./corpus"
  chunk_file: "./data/chunks.jsonl"
  output_dir: "./data/eval"

question_generation:
  questions_per_chunk: 2
  max_chunks: 200
  allowed_types:
    - concept
    - how_to
    - troubleshooting
    - parameter
    - comparison
    - limitation

candidate_pool:
  neighbor_window: 2
  bm25_top_k: 50
  vector_top_k: 50
  title_match_top_k: 10

card_filter:
  max_cards_per_question: 30
  snippet_chars: 240
  max_chunks_per_source: 5

llm_judge:
  relevance_threshold: 2
  batch_size: 20

review:
  sample_size: 50
  stratify_by:
    - question_type
    - difficulty

evaluation:
  top_k: [1, 3, 5, 10]
  run_generation: true
  run_llm_judge: true
```

## 9. 质量控制要求

- 问题生成后需要过滤过宽泛问题。
- 支持基于文本相似度或 embedding 的问题去重。
- 不应把 LLM 判断为 `is_answerable=false` 的样本放入正式评测集。
- 自动生成评测集应区分：
  - synthetic dev set；
  - weakly-supervised eval set；
  - human golden set。
- 最终报告中应分别展示不同集合上的指标。
- 至少支持导出一批人工审核样本，用于 sanity check。

## 10. 安全与稳定性要求

- API Key 只能通过环境变量或本地配置读取，不得写入日志和报告。
- LLM 调用失败不能导致整个流程不可恢复，应保存失败样本和错误原因。
- JSON 解析失败应支持重试或保存原始响应供人工排查。
- 所有中间文件应可复用，避免重复调用 LLM 造成成本浪费。
- 支持 `--limit` 小批量运行，降低调试成本。

## 11. 推荐输出目录

```text
data/eval/
  questions.jsonl
  candidate_pools.jsonl
  evidence_cards.jsonl
  evidence_judgments.jsonl
  eval_dataset_draft.jsonl
  eval_dataset.jsonl
  review_samples.md
  runs/
    run_YYYYMMDD_HHMMSS/
      retrieval_results.jsonl
      generation_results.jsonl
      metrics.json
      report.md
```

## 12. 验收标准

最小可用版本需要满足：

- 可以从现有 corpus 生成候选问题。
- 可以为问题构建多路候选证据池。
- 可以调用 OpenAI-compatible API 进行证据判断和答案要点归纳。
- 可以生成固定格式的 `eval_dataset.jsonl`。
- 可以基于固定评测集运行 RAG 检索评估。
- 可以输出至少 Evidence Hit@K、Evidence Recall@K、MRR、Must-have Coverage 和 latency。
- 每个步骤可以单独执行。

完整版本需要进一步满足：

- 支持 LLM-as-Judge 多维度评分。
- 支持人工审核集导出和审核结果回填。
- 支持不同 RAG 配置的横向对比。
- 支持按问题类型、难度和文档来源分组报告。
- 支持 token 成本统计。

## 13. 面试表达价值

该需求实现后，可以在简历或面试中表述为：

> 构建 RAG 离线评测集生成与指标验证流程，基于领域文档自动生成候选问题，通过多路高召回证据池、LLM 相关性筛选和答案要点归纳生成多证据支持的弱监督评测集，并结合人工抽样审核降低自举偏置。评测阶段覆盖 Evidence Hit@K、Evidence Recall@K、MRR、must-have coverage、LLM-as-Judge 和端到端延迟，用于指导 chunk 策略、混合检索权重、rerank 参数和 prompt 优化。
