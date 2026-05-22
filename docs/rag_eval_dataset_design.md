# RAG 评测集生成与指标验证脚本设计文档

## 1. 设计目标

本文基于 `docs/rag_eval_dataset_requirements.md`，设计一套离线 RAG 评测集生成与指标验证脚本。该设计面向 `ms_rag` 现有工程结构，复用已有索引、检索、生成和评测能力，同时新增分步执行的评测数据构造链路。

核心目标：

- 每一步可独立执行、可恢复、可复用中间产物。
- 支持 OpenAI-compatible Chat Completions API。
- 通过多路候选证据池和 LLM 弱监督标注降低自举偏置。
- 输出固定 `eval_dataset.jsonl`，用于复现实验和配置对比。
- 兼容现有 `RAGPipeline`、`HybridRetriever`、`BM25Index`、`VectorStore` 和 `scripts/evaluate.py`。

## 2. 当前系统可复用能力

### 2.1 现有索引构建能力

`D:/Project/ms_rag/scripts/build_index.py` 已提供：

- 从 `corpus/` 加载文档；
- 文本清洗；
- 父 chunk / 子 chunk 切分；
- embedding 生成；
- Chroma 向量库写入；
- BM25 索引构建；
- DocumentStore 父 chunk 存储；
- `graph.json` 文档关系图生成；
- `index_state.json` 增量索引状态。

评测集生成脚本应尽量读取这些已有产物，而不是重新定义一套索引格式。

### 2.2 现有检索能力

`D:/Project/ms_rag/src/retrieval/hybrid_retriever.py` 已提供：

- Chroma vector search；
- BM25 keyword search；
- 结果融合；
- 父 chunk 回填；
- `HybridResult` 统一结果结构。

候选证据池构建阶段可以复用底层 `VectorStore` 和 `BM25Index`，但不直接使用线上最终 top-k 作为唯一证据来源。

### 2.3 现有 RAG Pipeline

`D:/Project/ms_rag/src/pipeline/rag_pipeline.py` 已提供：

- query embedding；
- hybrid retrieval；
- rerank；
- KG enhance；
- context build；
- prompt render；
- LLM generation；
- cache；
- source 构建。

最终评测阶段可以调用 `RAGPipeline.query()` 获取端到端答案，也可以直接复用内部组件进行 retrieval-only 评估。

### 2.4 现有评测脚本

`D:/Project/ms_rag/scripts/evaluate.py` 已具备：

- Recall@K；
- Precision@K；
- MRR；
- NDCG@K；
- ROUGE-L；
- BERTScore；
- Keyword Coverage；
- LLM-as-Judge；
- latency 统计。

新设计不应完全替代该脚本，而应将其升级为可读取新评测集格式，或新增 `rag_eval_dataset.py evaluate` 子命令复用其中指标计算逻辑。

## 3. 总体架构

```text
corpus / existing index
        |
        v
[1] generate-questions
        |
        v
questions.jsonl
        |
        v
[2] build-evidence-pool
        |
        v
candidate_pools.jsonl
        |
        v
[3] build-evidence-cards
        |
        v
evidence_cards.jsonl
        |
        v
[4] judge-evidence
        |
        v
evidence_judgments.jsonl
        |
        v
[5] synthesize-answers
        |
        v
eval_dataset_draft.jsonl
        |
        +--> [6] export-review-set --> review_samples.md
        |
        v
manual review / optional approval
        |
        v
eval_dataset.jsonl
        |
        v
[7] evaluate
        |
        v
runs/<run_id>/metrics.json + report.md
```

## 4. CLI 设计

新增统一入口：

```text
scripts/rag_eval_dataset.py
```

推荐子命令：

```bash
python scripts/rag_eval_dataset.py generate-questions --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py build-evidence-pool --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py build-evidence-cards --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py judge-evidence --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py synthesize-answers --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py export-review-set --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py finalize-dataset --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py evaluate --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py report --config config/rag_eval.yaml
```

通用参数：

```bash
--config config/rag_eval.yaml
--limit 20
--offset 0
--input <path>
--output <path>
--dry-run
--force
--verbose
```

设计约束：

- 每个子命令只读取上一步产物，不依赖内存状态。
- 每个子命令输出 JSONL，便于追加、失败恢复和局部重跑。
- 如果输出文件已存在，默认跳过已处理 `id`；`--force` 才覆盖。
- `--limit` 用于低成本调试。
- LLM 调用类命令必须保存失败样本到 `failed_*.jsonl`。

## 5. 模块设计

建议新增包：

```text
src/evaluation/
  __init__.py
  config.py
  schemas.py
  io.py
  chunk_source.py
  openai_client.py
  prompt_templates.py
  question_generator.py
  evidence_pool.py
  evidence_cards.py
  evidence_judge.py
  answer_synthesizer.py
  review_exporter.py
  dataset_finalizer.py
  metrics.py
  runner.py
  reporter.py
```

脚本入口：

```text
scripts/rag_eval_dataset.py
```

### 5.1 `config.py`

职责：

- 读取 `config/rag_eval.yaml`；
- 支持环境变量展开；
- 提供类型化配置对象；
- 对路径、top_k、batch_size 等参数做基础校验。

关键配置模型：

```text
RagEvalConfig
  paths
  llm
  question_generation
  candidate_pool
  card_filter
  llm_judge
  synthesis
  review
  evaluation
```

### 5.2 `schemas.py`

定义所有中间产物的数据结构：

- `ChunkRecord`
- `GeneratedQuestion`
- `CandidateChunk`
- `CandidatePool`
- `EvidenceCard`
- `EvidenceCardSet`
- `EvidenceJudgment`
- `AnswerKeyPoint`
- `EvalSample`
- `EvaluationResult`
- `MetricSummary`

推荐使用 Pydantic，原因：

- LLM JSON 输出需要强校验；
- 中间文件需要稳定 schema；
- 错误信息更利于排查。

### 5.3 `io.py`

职责：

- JSONL 读写；
- 根据 `id` 跳过已存在记录；
- 原子写入临时文件后 rename；
- 保存 LLM raw response；
- 保存失败样本。

### 5.4 `chunk_source.py`

职责：统一提供可用于评测生成的 chunk 视图。

数据来源优先级：

1. 优先读取已有 DocumentStore / VectorStore / BM25 产物；
2. 若现有索引不方便反查，则复用 `DocumentLoader`、`TextCleaner`、`DocumentSplitter` 从 `corpus/` 生成临时 chunk records；
3. chunk id 应尽量与现有索引保持一致，否则评测检索指标无法对齐。

输出字段：

```json
{
  "chunk_id": "...",
  "doc_id": "...",
  "source_file": "...",
  "doc_title": "...",
  "section_title": "...",
  "section_path": "...",
  "content": "...",
  "parent_id": "...",
  "prev_chunk_id": "...",
  "next_chunk_id": "..."
}
```

### 5.5 `openai_client.py`

职责：封装 OpenAI-compatible Chat Completions API。

接口：

```text
chat_json(messages, response_schema=None, temperature=None, max_tokens=None) -> dict
chat_text(messages, temperature=None, max_tokens=None) -> str
```

要求：

- 支持 `base_url`；
- 支持 `api_key`；
- 支持 `model`；
- 支持 timeout；
- 支持 max retries；
- 支持指数退避；
- 支持从 markdown code block 中提取 JSON；
- 不记录 API Key；
- 原始响应可选落盘。

由于项目已有 `src/generation/llm_service.py`，设计上有两种选择：

- MVP：新增独立 `OpenAICompatibleClient`，避免影响线上 LLMService；
- 后续：将 OpenAI-compatible 能力合并回 `LLMService`。

推荐 MVP 采用独立 client，降低对现有问答链路的影响。

### 5.6 `question_generator.py`

输入：`ChunkRecord`。

输出：`GeneratedQuestion`。

职责：

- 从 chunk 生成 1-N 个候选问题；
- 控制问题类型分布；
- 过滤过短、过宽泛、不可回答问题；
- 生成关键词、难度和类型标签。

执行策略：

```text
for chunk in chunks:
  if chunk too short: skip
  prompt LLM with chunk metadata + content
  parse questions
  validate question specificity
  write questions.jsonl
```

质量规则：

- 问题不能是“如何进行性能优化”这类泛化问题；
- 问题必须能从当前 chunk 或相关文档回答；
- 每个问题保留 `seed_chunk_id`。

### 5.7 `evidence_pool.py`

输入：`GeneratedQuestion`。

输出：`CandidatePool`。

职责：构建高召回候选证据池。

候选来源：

```text
seed chunk
seed neighbor chunks
same document / same section chunks
BM25 top_k
Vector top_k
title / keyword match top_k
```

注意：

- 这里不能只调用线上 `RAGPipeline.query()` 或线上最终 top-k。
- 这里应调用底层 `BM25Index.search()` 和 `VectorStore.search()`，并扩大 top-k。
- 候选池用于评测集构造，允许召回更多噪声。

候选去重规则：

- 以 `chunk_id` 去重；
- 合并 `origin`；
- 保留各路 rank 和 score；
- seed chunk 和邻近 chunk 强制保留。

### 5.8 `evidence_cards.py`

输入：`CandidatePool`。

输出：`EvidenceCardSet`。

职责：在 LLM 判断前进行粗筛和压缩。

流程：

```text
candidate chunks
  -> score normalization
  -> weighted ranking
  -> per-source diversity limit
  -> top N
  -> snippet extraction
  -> evidence card output
```

综合分建议：

```text
score =
  bm25_weight * normalized_bm25_score
+ vector_weight * normalized_vector_score
+ title_match_bonus
+ same_doc_bonus
+ seed_neighbor_bonus
```

Evidence Card 不传完整 chunk，只传：

- chunk_id；
- source_file；
- doc_title；
- section_path；
- matched_keywords；
- snippet；
- rank/score。

### 5.9 `evidence_judge.py`

输入：`EvidenceCardSet`。

输出：`EvidenceJudgment`。

职责：让 LLM 判断 evidence card 是否支持回答问题。

LLM 任务边界：

- 只判断相关性；
- 不生成最终答案；
- 不引入外部知识；
- 对每个 card 输出 `relevance`、`supported_points`、`reason`。

相关性等级：

```text
0 = unrelated
1 = topic_related_but_not_answering
2 = partially_supporting
3 = directly_supporting
```

筛选规则：

- `relevance >= threshold` 的 chunk 进入答案归纳；
- 如果没有 chunk 达标，该问题标记为证据不足。

### 5.10 `answer_synthesizer.py`

输入：`EvidenceJudgment` + selected full chunks。

输出：`EvalSample` draft。

职责：基于少量完整 supporting chunks 生成标准评测样本。

输出内容：

- `question`；
- `question_type`；
- `difficulty`；
- `answer_key_points`；
- `must_have_points`；
- `nice_to_have_points`；
- `expected_answer`；
- `acceptable_chunk_ids`；
- `acceptable_source_files`；
- `keywords`；
- `is_answerable`；
- `conflicts`。

设计约束：

- 每个 key point 尽量绑定 supporting chunks；
- 不允许使用文档外知识；
- 如果 supporting chunks 不足，输出 `is_answerable=false`；
- `must_have_points` 不宜过多，建议 2-5 条；
- `nice_to_have_points` 用于完整性加分，不作为硬性检索标准。

### 5.11 `review_exporter.py`

输入：`eval_dataset_draft.jsonl`。

输出：`review_samples.md` 或 `review_samples.jsonl`。

职责：导出人工审核样本。

抽样策略：

- 按 `question_type` 分层；
- 按 `difficulty` 分层；
- 按 source 分散；
- 支持随机种子保证复现。

Markdown 格式应包含：

- 问题；
- 类型/难度；
- expected answer；
- must-have points；
- nice-to-have points；
- supporting chunks 摘要；
- 人工审核字段。

### 5.12 `dataset_finalizer.py`

职责：生成最终固定评测集。

输入来源：

- 自动草稿集；
- 可选人工审核结果。

规则：

- `is_answerable=false` 不进入正式集；
- `rejected` 不进入正式集；
- `needs_edit` 如果未修正，不进入正式集；
- `approved` 优先进入 human golden set；
- 未审核样本可进入 weakly-supervised eval set。

输出：

```text
data/eval/eval_dataset.jsonl
data/eval/eval_dataset_weak.jsonl
data/eval/eval_dataset_golden.jsonl
```

### 5.13 `metrics.py`

职责：统一指标计算。

检索指标：

- Evidence Hit@K；
- Evidence Recall@K；
- MRR；
- NDCG@K。

生成指标：

- Must-have Coverage；
- Nice-to-have Coverage；
- Keyword Coverage；
- LLM-as-Judge correctness；
- LLM-as-Judge faithfulness；
- LLM-as-Judge completeness；
- LLM-as-Judge relevance。

建议将 `scripts/evaluate.py` 中已有指标迁移或复用到该模块，避免重复实现。

### 5.14 `runner.py`

职责：运行固定评测集。

流程：

```text
load eval_dataset.jsonl
initialize RAGPipeline
for each sample:
  run retrieval-only
  calculate retrieval metrics
  optionally run full query
  calculate must-have / keyword coverage
  optionally run LLM-as-Judge
  write per-sample result
aggregate metrics
```

retrieval-only 建议直接使用：

```text
pipeline.embedding_service.embed_query
pipeline.retriever.retrieve
pipeline.reranker.rerank
pipeline.kg_enhancer.enhance
```

这样可以记录每个阶段耗时。

### 5.15 `reporter.py`

职责：生成报告。

输出：

- `metrics.json`；
- `report.md`；
- per-case details；
- group-by summaries。

报告维度：

- overall；
- by question_type；
- by difficulty；
- by source_file；
- by dataset split；
- by RAG config name。

## 6. 配置设计

新增配置文件：

```text
config/rag_eval.yaml
```

建议结构：

```yaml
paths:
  corpus_dir: "./corpus"
  output_dir: "./data/eval"
  system_config: "./config/system.yaml"
  raw_response_dir: "./data/eval/raw_llm"

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
  save_raw_response: true

question_generation:
  questions_per_chunk: 2
  max_chunks: 200
  min_chunk_chars: 200
  allowed_types: [concept, how_to, troubleshooting, parameter, comparison, limitation]

candidate_pool:
  neighbor_window: 2
  same_section_limit: 8
  bm25_top_k: 50
  vector_top_k: 50
  title_match_top_k: 10

card_filter:
  max_cards_per_question: 30
  snippet_chars: 240
  max_chunks_per_source: 5
  bm25_weight: 0.35
  vector_weight: 0.35
  title_match_bonus: 0.1
  same_doc_bonus: 0.1
  seed_neighbor_bonus: 0.1

llm_judge:
  relevance_threshold: 2
  batch_size: 20

synthesis:
  max_supporting_chunks: 8
  max_chunk_chars: 1200
  max_must_have_points: 5
  max_nice_to_have_points: 5

review:
  sample_size: 50
  random_seed: 42
  stratify_by: [question_type, difficulty]

evaluation:
  dataset_path: "./data/eval/eval_dataset.jsonl"
  top_k: [1, 3, 5, 10]
  run_generation: true
  run_llm_judge: true
  compare_configs: []
```

## 7. 数据流设计

### 7.1 中间文件目录

```text
data/eval/
  questions.jsonl
  candidate_pools.jsonl
  evidence_cards.jsonl
  evidence_judgments.jsonl
  eval_dataset_draft.jsonl
  eval_dataset.jsonl
  eval_dataset_weak.jsonl
  eval_dataset_golden.jsonl
  review_samples.md
  failed/
    generate_questions.jsonl
    judge_evidence.jsonl
    synthesize_answers.jsonl
  raw_llm/
    <step>/<record_id>.json
  runs/
    run_YYYYMMDD_HHMMSS/
      retrieval_results.jsonl
      generation_results.jsonl
      judge_results.jsonl
      metrics.json
      report.md
```

### 7.2 ID 设计

- question id: `q_<hash(seed_chunk_id + question)>`
- candidate pool id: question id
- eval sample id: `eval_<hash(question + acceptable_chunk_ids)>`
- run id: `run_YYYYMMDD_HHMMSS_<config_name>`

使用稳定 hash 可以避免重复运行产生大量重复样本。

## 8. Prompt 设计边界

Prompt 不放入业务代码中硬编码，建议集中在：

```text
src/evaluation/prompt_templates.py
```

或：

```text
config/rag_eval_prompts.yaml
```

推荐模板：

- `generate_questions_prompt`
- `judge_evidence_prompt`
- `synthesize_answer_prompt`
- `judge_answer_prompt`

关键约束：

- 要求输出严格 JSON；
- 明确禁止使用文档外知识；
- 明确区分“主题相关”和“能够支撑回答”；
- 对无法回答问题输出 `is_answerable=false`；
- 对冲突证据输出 `conflicts`。

## 9. 指标设计

### 9.1 Evidence Hit@K

```text
hit@k = 1 if top_k_retrieved intersects acceptable_chunk_ids else 0
```

### 9.2 Evidence Recall@K

```text
recall@k = |top_k_retrieved ∩ acceptable_chunk_ids| / |acceptable_chunk_ids|
```

### 9.3 MRR

```text
mrr = 1 / rank(first acceptable chunk)
```

### 9.4 NDCG@K

如果 evidence judgment 保存了 relevance，可用：

```text
rel = 3 for directly supporting
rel = 2 for partially supporting
```

否则 acceptable chunk 统一 `rel=1`。

### 9.5 Must-have Coverage

优先使用 LLM-as-Judge 判断同义覆盖；MVP 可用关键词/子串近似。

```text
coverage = covered_must_have_points / total_must_have_points
```

### 9.6 LLM-as-Judge

输入：

- question；
- retrieved contexts；
- expected answer；
- must-have points；
- model answer。

输出：

- correctness；
- faithfulness；
- completeness；
- relevance；
- hallucinated_claims；
- missed_must_have_points。

## 10. 防自举偏置设计

为避免“用被测系统构造数据，再用同一系统评测”导致指标虚高，设计上采用：

1. 构造阶段不直接使用线上最终 RAG top-k 作为唯一证据来源。
2. 候选证据池使用多路高召回：seed、邻近、同 section、BM25、Vector、标题匹配。
3. LLM 只从候选池中筛选证据，不凭空生成标准答案。
4. 最终评测集固定保存，评测时不再动态修改 acceptable evidence。
5. 支持 human golden set 抽样审核。
6. 报告区分 synthetic、weak、golden 三类数据集。

## 11. 与现有代码的集成方式

### 11.1 与 `build_index.py`

- 评测脚本不负责主索引构建。
- 使用前要求先运行现有 `scripts/build_index.py`。
- 如果索引不存在，评测脚本应报错并提示用户先构建索引。

### 11.2 与 `RAGPipeline`

- `evaluate` 子命令初始化 `RAGPipeline(settings)`。
- retrieval-only 评估复用 pipeline 内部组件。
- generation 评估调用 `pipeline.query(question, top_k)`。

### 11.3 与 `evaluate.py`

短期方案：

- 保留 `scripts/evaluate.py`；
- 新脚本单独实现新数据格式评测；
- 必要时复用其中指标计算函数。

长期方案：

- 将 `evaluate.py` 中通用指标迁移到 `src/evaluation/metrics.py`；
- `scripts/evaluate.py` 变成兼容旧格式的薄入口。

## 12. 错误处理设计

### 12.1 LLM 调用失败

- 按配置重试；
- 重试失败写入 `failed/<step>.jsonl`；
- 不阻断整个批次；
- 报告失败数量。

### 12.2 JSON 解析失败

- 尝试从 markdown code block 中提取 JSON；
- 尝试修剪 JSON 前后多余文本；
- 仍失败则保存 raw response；
- 写入失败文件。

### 12.3 中间产物不一致

- 如果问题引用的 seed chunk 不存在，应跳过并记录错误；
- 如果 acceptable chunk 在当前索引中不存在，评测时记录为 stale evidence；
- 报告 stale evidence 比例。

## 13. 实施阶段建议

### Phase 1: MVP

目标：跑通最小闭环。

范围：

- `config.py`
- `schemas.py`
- `io.py`
- `openai_client.py`
- `chunk_source.py`
- `question_generator.py`
- `evidence_pool.py`
- `evidence_judge.py`
- `answer_synthesizer.py`
- `runner.py` 的 retrieval-only 部分

验收：

```bash
python scripts/rag_eval_dataset.py generate-questions --limit 20
python scripts/rag_eval_dataset.py build-evidence-pool --limit 20
python scripts/rag_eval_dataset.py build-evidence-cards --limit 20
python scripts/rag_eval_dataset.py judge-evidence --limit 20
python scripts/rag_eval_dataset.py synthesize-answers --limit 20
python scripts/rag_eval_dataset.py evaluate --limit 20
```

输出 Evidence Hit@K、Evidence Recall@K、MRR、latency。

### Phase 2: 完整评测

增加：

- review exporter；
- finalizer；
- LLM-as-Judge；
- Must-have Coverage；
- Markdown report；
- group-by statistics。

### Phase 3: 配置对比与优化闭环

增加：

- 多 RAG 配置对比；
- BM25-only / Vector-only / Hybrid / Hybrid+Rerank 对比；
- hard negative 导出；
- token 成本统计；
- golden set 报告。

## 14. 设计取舍

### 14.1 为什么用统一 CLI 而不是多个脚本

统一 CLI 可以共享配置、schema、日志、错误处理和 IO 逻辑，同时仍然通过子命令满足“每一步单独执行”。

### 14.2 为什么新增 OpenAI-compatible client

评测数据构造是离线任务，对 JSON 输出、raw response、重试和失败恢复要求更强。独立 client 可以避免影响线上 `LLMService`。

### 14.3 为什么不把重型证据筛选作为线上 RAG 主链路

评测构造追求高召回和低偏置，可以接受高成本和高延迟；线上 RAG 追求低延迟、低成本、稳定响应。离线重流程应用于数据集构造和调参，不直接替代线上问答链路。

## 15. 最终产物

本设计完成后，项目应新增：

```text
config/rag_eval.yaml
scripts/rag_eval_dataset.py
src/evaluation/
  config.py
  schemas.py
  io.py
  chunk_source.py
  openai_client.py
  prompt_templates.py
  question_generator.py
  evidence_pool.py
  evidence_cards.py
  evidence_judge.py
  answer_synthesizer.py
  review_exporter.py
  dataset_finalizer.py
  metrics.py
  runner.py
  reporter.py
```

并生成运行产物：

```text
data/eval/eval_dataset.jsonl
data/eval/runs/<run_id>/metrics.json
data/eval/runs/<run_id>/report.md
```

## 16. 后续实现入口

建议从 Phase 1 MVP 开始实现，优先保证：

1. 配置可读；
2. OpenAI-compatible API 可调用；
3. JSONL 中间产物稳定；
4. 每一步可单独执行；
5. 能生成 20 条样本并完成 retrieval-only 指标计算。
