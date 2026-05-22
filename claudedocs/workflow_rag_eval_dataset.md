# RAG 评测集生成与指标验证脚本实施工作流

## 1. 工作流目标

基于以下文档实施 RAG 评测集生成与指标验证能力：

- `docs/rag_eval_dataset_requirements.md`
- `docs/rag_eval_dataset_design.md`

本工作流只定义实施顺序、依赖关系、检查点和验证方式，不包含具体实现代码。

目标产物：

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

运行产物：

```text
data/eval/questions.jsonl
data/eval/candidate_pools.jsonl
data/eval/evidence_cards.jsonl
data/eval/evidence_judgments.jsonl
data/eval/eval_dataset_draft.jsonl
data/eval/eval_dataset.jsonl
data/eval/runs/<run_id>/metrics.json
data/eval/runs/<run_id>/report.md
```

## 2. 总体阶段划分

```text
Phase 0: 实施前检查
Phase 1: 基础设施层
Phase 2: 问题生成链路
Phase 3: 候选证据池与 evidence card 链路
Phase 4: LLM 证据判断与答案归纳链路
Phase 5: 固定评测集与 retrieval-only 评估
Phase 6: 人工审核、LLM-as-Judge 与报告增强
Phase 7: 配置对比与优化闭环
```

建议先完成 Phase 1-5，形成 MVP 闭环；Phase 6-7 作为增强阶段。

## 3. Phase 0：实施前检查

### 3.1 目标

确认现有 RAG 索引、配置和依赖可用，避免后续脚本因基础数据缺失失败。

### 3.2 任务

1. 检查 `config/system.yaml` 是否存在且可被 `get_settings()` 读取。
2. 检查 `corpus/` 是否存在文档。
3. 检查现有索引是否存在：
   - Chroma persist directory；
   - BM25 index；
   - DocumentStore；
   - `graph.json` 可选。
4. 如索引不存在，先运行现有：

```bash
python scripts/build_index.py --config ./config/system.yaml
```

### 3.3 验证检查点

- `RAGPipeline(settings)` 可以初始化。
- `pipeline.retriever.retrieve(...)` 可以返回结果。
- `scripts/evaluate.py` 仍可保持原有行为。

### 3.4 阻塞关系

Phase 0 是所有后续阶段的前置条件。

## 4. Phase 1：基础设施层

### 4.1 目标

实现所有后续步骤共享的配置、schema、JSONL IO、OpenAI-compatible client 和 CLI 框架。

### 4.2 任务清单

#### T1.1 新增配置文件

文件：

```text
config/rag_eval.yaml
```

内容覆盖：

- paths；
- llm；
- question_generation；
- candidate_pool；
- card_filter；
- llm_judge；
- synthesis；
- review；
- evaluation。

依赖：无。

验收：

- 支持 `${OPENAI_BASE_URL}`、`${OPENAI_API_KEY}`、`${OPENAI_MODEL}` 环境变量。
- 默认输出目录为 `data/eval/`。

#### T1.2 新增类型化配置读取

文件：

```text
src/evaluation/config.py
```

职责：

- 读取 yaml；
- 展开环境变量；
- 提供配置对象；
- 校验关键路径和数值范围。

依赖：T1.1。

验收：

- 可以通过 `load_eval_config("config/rag_eval.yaml")` 读取配置。
- API Key 不应在 repr 或日志中明文输出。

#### T1.3 新增 Pydantic schema

文件：

```text
src/evaluation/schemas.py
```

核心模型：

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

依赖：无。

验收：

- 所有 JSONL 中间产物都有对应模型。
- LLM 输出解析失败能暴露清晰字段错误。

#### T1.4 新增 JSONL IO 工具

文件：

```text
src/evaluation/io.py
```

职责：

- read_jsonl；
- append_jsonl；
- write_jsonl_atomic；
- load_existing_ids；
- write_failed_record；
- save_raw_response。

依赖：T1.3。

验收：

- 支持按 `id` 跳过已处理记录。
- 支持失败样本写入 `data/eval/failed/`。
- 支持 raw response 写入 `data/eval/raw_llm/`。

#### T1.5 新增 OpenAI-compatible client

文件：

```text
src/evaluation/openai_client.py
```

职责：

- 调用 OpenAI-compatible Chat Completions API；
- 支持 JSON 输出解析；
- 支持 timeout、retry、backoff；
- 支持 raw response 保存；
- 不泄露 API Key。

依赖：T1.2、T1.4。

验收：

- 支持自定义 `base_url`、`model`、`api_key`。
- `chat_json()` 能从 markdown code block 中提取 JSON。
- 网络失败或 JSON 解析失败可重试并记录失败。

#### T1.6 新增 CLI 入口骨架

文件：

```text
scripts/rag_eval_dataset.py
```

子命令先注册但可暂时为空：

- generate-questions；
- build-evidence-pool；
- build-evidence-cards；
- judge-evidence；
- synthesize-answers；
- export-review-set；
- finalize-dataset；
- evaluate；
- report。

依赖：T1.2。

验收：

```bash
python scripts/rag_eval_dataset.py --help
python scripts/rag_eval_dataset.py generate-questions --help
```

均能正常输出帮助信息。

### 4.3 Phase 1 质量门禁

- 不调用真实 RAG Pipeline 也能运行 CLI help。
- 不需要真实 API Key 也能加载配置，但调用 LLM 时应检测缺失并报错。
- 单元测试应覆盖：配置读取、JSONL IO、schema 校验、JSON 提取。

## 5. Phase 2：问题生成链路

### 5.1 目标

从现有 corpus / chunk 数据中生成候选问题，输出 `questions.jsonl`。

### 5.2 任务清单

#### T2.1 新增 chunk source

文件：

```text
src/evaluation/chunk_source.py
```

职责：

- 提供统一 `ChunkRecord`；
- 尽量保持 chunk_id 与现有索引一致；
- 支持从 DocumentStore / corpus fallback 加载 chunk；
- 建立 prev / next / same doc / same section 关系。

依赖：T1.2、T1.3。

验收：

- 可以输出 N 条 `ChunkRecord`。
- 每条记录至少包含 `chunk_id`、`source_file`、`content`。
- 支持 `--limit` 调试。

#### T2.2 新增问题生成 prompt

文件：

```text
src/evaluation/prompt_templates.py
```

新增模板：

- `generate_questions_prompt`。

依赖：T1.3。

验收：

- Prompt 明确要求严格 JSON。
- Prompt 明确禁止生成过宽泛问题。
- Prompt 要求输出 question_type、difficulty、keywords。

#### T2.3 新增 question generator

文件：

```text
src/evaluation/question_generator.py
```

职责：

- 遍历 chunk；
- 调用 LLM 生成问题；
- 基础过滤；
- 生成稳定 question id；
- 写入 `questions.jsonl`。

依赖：T1.5、T2.1、T2.2。

验收：

```bash
python scripts/rag_eval_dataset.py generate-questions --config config/rag_eval.yaml --limit 5
```

输出：

```text
data/eval/questions.jsonl
```

每条记录包含：

- id；
- question；
- seed_chunk_id；
- seed_source_file；
- question_type；
- difficulty；
- keywords。

### 5.3 Phase 2 质量门禁

- 生成问题不能全部集中在同一文档。
- 过短 chunk 应跳过。
- LLM 失败样本进入 failed 文件，不阻断批次。

## 6. Phase 3：候选证据池与 Evidence Card 链路

### 6.1 目标

为每个问题构建高召回候选证据池，再压缩为 LLM 可处理的 evidence cards。

### 6.2 任务清单

#### T3.1 新增 evidence pool builder

文件：

```text
src/evaluation/evidence_pool.py
```

候选来源：

- seed chunk；
- seed neighbor chunks；
- same document / same section；
- BM25 top-k；
- Vector top-k；
- title / keyword match。

依赖：T2.1、T2.3、现有 `BM25Index`、`VectorStore`、`EmbeddingService`。

验收：

```bash
python scripts/rag_eval_dataset.py build-evidence-pool --config config/rag_eval.yaml --limit 5
```

输出：

```text
data/eval/candidate_pools.jsonl
```

每条记录包含：

- question_id；
- candidate_chunks；
- origin；
- bm25 rank / score；
- vector rank / score。

#### T3.2 新增 evidence card builder

文件：

```text
src/evaluation/evidence_cards.py
```

职责：

- 归一化分数；
- 综合排序；
- source diversity 限制；
- snippet 抽取；
- 输出 evidence cards。

依赖：T3.1。

验收：

```bash
python scripts/rag_eval_dataset.py build-evidence-cards --config config/rag_eval.yaml --limit 5
```

输出：

```text
data/eval/evidence_cards.jsonl
```

每个问题最多保留配置指定数量的 cards，例如 30 个。

### 6.3 Phase 3 质量门禁

- seed chunk 必须保留。
- 候选池去重后不应为空。
- evidence card snippet 不应超过配置长度。
- 不允许把完整 80+ chunk 直接塞给 LLM。

## 7. Phase 4：LLM 证据判断与答案归纳链路

### 7.1 目标

让 LLM 对 evidence cards 做相关性判断，再基于少量 supporting chunks 生成最终评测样本草稿。

### 7.2 任务清单

#### T4.1 新增 evidence judge prompt

文件：

```text
src/evaluation/prompt_templates.py
```

新增模板：

- `judge_evidence_prompt`。

依赖：T2.2。

验收：

- Prompt 明确 relevance 0-3 定义。
- Prompt 明确“主题相关但不能回答”不算 supporting evidence。
- Prompt 要求输出 JSON。

#### T4.2 新增 evidence judge

文件：

```text
src/evaluation/evidence_judge.py
```

职责：

- 按 batch 调用 LLM；
- 解析每个 card 的 relevance；
- 保留 supported_points 和 reason；
- 写入 `evidence_judgments.jsonl`。

依赖：T1.5、T3.2、T4.1。

验收：

```bash
python scripts/rag_eval_dataset.py judge-evidence --config config/rag_eval.yaml --limit 5
```

输出：

```text
data/eval/evidence_judgments.jsonl
```

#### T4.3 新增 answer synthesis prompt

文件：

```text
src/evaluation/prompt_templates.py
```

新增模板：

- `synthesize_answer_prompt`。

依赖：T4.1。

验收：

- Prompt 要求基于 supporting chunk 原文归纳。
- Prompt 明确禁止文档外知识。
- Prompt 要求每个 answer key point 绑定 supporting chunk。

#### T4.4 新增 answer synthesizer

文件：

```text
src/evaluation/answer_synthesizer.py
```

职责：

- 根据 evidence judgment 选择 relevance >= threshold 的 chunks；
- 加载完整 chunk 原文；
- 调用 LLM 生成 `EvalSample`；
- 写入 `eval_dataset_draft.jsonl`。

依赖：T2.1、T4.2、T4.3。

验收：

```bash
python scripts/rag_eval_dataset.py synthesize-answers --config config/rag_eval.yaml --limit 5
```

输出：

```text
data/eval/eval_dataset_draft.jsonl
```

### 7.3 Phase 4 质量门禁

- `is_answerable=false` 样本保留在 draft，但后续不能进入正式集。
- `acceptable_chunk_ids` 必须来自 supporting chunks。
- `must_have_points` 不宜超过配置上限。
- JSON 解析失败不应中断整个批次。

## 8. Phase 5：固定评测集与 Retrieval-only 评估

### 8.1 目标

生成固定 `eval_dataset.jsonl`，并实现 retrieval-only 指标计算，完成 MVP 闭环。

### 8.2 任务清单

#### T5.1 新增 dataset finalizer MVP

文件：

```text
src/evaluation/dataset_finalizer.py
```

MVP 规则：

- 过滤 `is_answerable=false`；
- 过滤 `acceptable_chunk_ids` 为空；
- 输出 `eval_dataset.jsonl`；
- 暂不要求人工审核回填。

依赖：T4.4。

验收：

```bash
python scripts/rag_eval_dataset.py finalize-dataset --config config/rag_eval.yaml
```

输出：

```text
data/eval/eval_dataset.jsonl
```

#### T5.2 新增 metrics MVP

文件：

```text
src/evaluation/metrics.py
```

实现：

- Evidence Hit@K；
- Evidence Recall@K；
- MRR；
- NDCG@K；
- latency aggregation。

依赖：T1.3。

验收：

- 用固定 retrieved ids 和 acceptable ids 的测试样例验证结果。

#### T5.3 新增 runner retrieval-only

文件：

```text
src/evaluation/runner.py
```

职责：

- 加载 `eval_dataset.jsonl`；
- 初始化 `RAGPipeline`；
- 执行 retrieval-only；
- 记录 retrieved ids；
- 计算指标；
- 写入 run 目录。

依赖：T5.1、T5.2、现有 `RAGPipeline`。

验收：

```bash
python scripts/rag_eval_dataset.py evaluate --config config/rag_eval.yaml --limit 5
```

输出：

```text
data/eval/runs/<run_id>/retrieval_results.jsonl
data/eval/runs/<run_id>/metrics.json
```

#### T5.4 新增 report MVP

文件：

```text
src/evaluation/reporter.py
```

MVP 输出：

- 总样本数；
- Evidence Hit@K；
- Evidence Recall@K；
- MRR；
- 平均 retrieval latency。

依赖：T5.3。

验收：

```bash
python scripts/rag_eval_dataset.py report --config config/rag_eval.yaml
```

输出：

```text
data/eval/runs/<run_id>/report.md
```

### 8.3 Phase 5 质量门禁

MVP 通过条件：

```bash
python scripts/rag_eval_dataset.py generate-questions --limit 20
python scripts/rag_eval_dataset.py build-evidence-pool --limit 20
python scripts/rag_eval_dataset.py build-evidence-cards --limit 20
python scripts/rag_eval_dataset.py judge-evidence --limit 20
python scripts/rag_eval_dataset.py synthesize-answers --limit 20
python scripts/rag_eval_dataset.py finalize-dataset
python scripts/rag_eval_dataset.py evaluate --limit 20
python scripts/rag_eval_dataset.py report
```

可以生成：

- `eval_dataset.jsonl`；
- `metrics.json`；
- `report.md`。

## 9. Phase 6：人工审核、LLM-as-Judge 与报告增强

### 9.1 目标

增强评测可信度和可解释性。

### 9.2 任务清单

#### T6.1 Review exporter

文件：

```text
src/evaluation/review_exporter.py
```

输出：

```text
data/eval/review_samples.md
```

依赖：T4.4。

验收：

- 支持按 question_type / difficulty 分层抽样。
- Markdown 包含问题、标准答案、must-have points、supporting chunk 摘要和审核字段。

#### T6.2 Finalizer 支持人工审核结果

文件：

```text
src/evaluation/dataset_finalizer.py
```

增强：

- 支持 approved / rejected / needs_edit；
- 输出 weak / golden 两类数据集。

依赖：T6.1。

验收：

```text
data/eval/eval_dataset_weak.jsonl
data/eval/eval_dataset_golden.jsonl
```

#### T6.3 LLM-as-Judge 生成质量评估

涉及文件：

```text
src/evaluation/prompt_templates.py
src/evaluation/runner.py
src/evaluation/metrics.py
```

新增：

- correctness；
- faithfulness；
- completeness；
- relevance；
- hallucinated_claims；
- missed_must_have_points。

依赖：T5.3。

验收：

- `evaluation.run_llm_judge=true` 时运行。
- judge 失败不影响 retrieval 指标。

#### T6.4 Must-have / Nice-to-have Coverage

文件：

```text
src/evaluation/metrics.py
```

实现：

- MVP 可先用规则或关键词近似；
- 完整版使用 LLM-as-Judge 输出覆盖情况。

依赖：T6.3。

#### T6.5 报告增强

文件：

```text
src/evaluation/reporter.py
```

新增分组：

- by question_type；
- by difficulty；
- by source_file；
- by dataset split。

依赖：T6.2、T6.3。

### 9.3 Phase 6 质量门禁

- 可以区分 weak set 与 golden set。
- 报告中不只给总分，还给分组指标。
- LLM-as-Judge 原始响应可追溯。

## 10. Phase 7：配置对比与优化闭环

### 10.1 目标

支持不同 RAG 配置横向对比，为简历和面试提供可解释实验结果。

### 10.2 任务清单

#### T7.1 多配置评估

增强：

```text
src/evaluation/runner.py
```

支持：

- BM25-only；
- Vector-only；
- Hybrid；
- Hybrid + Rerank；
- 不同 top_k；
- 不同 vector_weight / keyword_weight。

依赖：T5.3。

#### T7.2 Hard negatives 导出

新增功能：

- 对 relevance=0/1 但排序靠前的 chunk 标记为 hard negative；
- 输出 hard negative 数据，用于后续 reranker 优化。

依赖：T4.2、T5.3。

#### T7.3 成本统计

增强：

- 统计 LLM 调用次数；
- 估算 prompt / completion tokens；
- 统计平均每条样本构造成本。

依赖：T1.5、T6.3。

#### T7.4 对比报告

增强：

```text
src/evaluation/reporter.py
```

输出：

- 配置对比表；
- 指标变化；
- 延迟变化；
- hard negative 示例。

### 10.3 Phase 7 质量门禁

- 至少可以比较 BM25-only、Vector-only、Hybrid 三种配置。
- 报告能说明不同问题类型下哪类策略更有效。

## 11. 任务依赖图

```text
Phase 0
  |
  v
T1.1 -> T1.2 -> T1.5 -> T2.3 -> T4.2 -> T4.4 -> T5.1 -> T5.3 -> T5.4
          |       |       |       |       |
          |       |       |       |       +-> T6.1 -> T6.2
          |       |       |       +-> T6.3 -> T6.4 -> T6.5
          |       |       +-> T3.1 -> T3.2
          |       +-> T1.4
          +-> T1.3 -> T5.2

T2.1 -> T2.3
T2.1 -> T3.1
T3.1 -> T3.2
T3.2 -> T4.2
T4.2 -> T4.4
T5.3 -> T7.1 -> T7.4
T4.2 + T5.3 -> T7.2
T1.5 + T6.3 -> T7.3
```

## 12. 推荐执行顺序

### MVP 执行顺序

1. T1.1 配置文件
2. T1.2 配置读取
3. T1.3 schema
4. T1.4 JSONL IO
5. T1.5 OpenAI-compatible client
6. T1.6 CLI 骨架
7. T2.1 chunk source
8. T2.2 prompt templates
9. T2.3 question generator
10. T3.1 evidence pool builder
11. T3.2 evidence card builder
12. T4.1 evidence judge prompt
13. T4.2 evidence judge
14. T4.3 synthesis prompt
15. T4.4 answer synthesizer
16. T5.1 dataset finalizer MVP
17. T5.2 metrics MVP
18. T5.3 runner retrieval-only
19. T5.4 report MVP

### 增强阶段执行顺序

20. T6.1 review exporter
21. T6.2 finalizer 审核增强
22. T6.3 LLM-as-Judge
23. T6.4 coverage metrics
24. T6.5 report group-by
25. T7.1 多配置评估
26. T7.2 hard negatives
27. T7.3 成本统计
28. T7.4 对比报告

## 13. 测试策略

### 13.1 单元测试

优先覆盖：

- config 环境变量展开；
- schema 校验；
- JSONL 读写；
- JSON 提取；
- metrics 计算；
- evidence card 排序和截断。

建议新增：

```text
tests/test_rag_eval_config.py
tests/test_rag_eval_io.py
tests/test_rag_eval_schemas.py
tests/test_rag_eval_metrics.py
tests/test_rag_eval_evidence_cards.py
```

### 13.2 集成测试

使用 `--limit 2` 和 mock LLM client 跑通：

```text
generate-questions
build-evidence-pool
build-evidence-cards
judge-evidence
synthesize-answers
finalize-dataset
evaluate
```

### 13.3 手工验收

使用真实 OpenAI-compatible API 跑：

```bash
python scripts/rag_eval_dataset.py generate-questions --config config/rag_eval.yaml --limit 5
python scripts/rag_eval_dataset.py build-evidence-pool --config config/rag_eval.yaml --limit 5
python scripts/rag_eval_dataset.py build-evidence-cards --config config/rag_eval.yaml --limit 5
python scripts/rag_eval_dataset.py judge-evidence --config config/rag_eval.yaml --limit 5
python scripts/rag_eval_dataset.py synthesize-answers --config config/rag_eval.yaml --limit 5
python scripts/rag_eval_dataset.py finalize-dataset --config config/rag_eval.yaml
python scripts/rag_eval_dataset.py evaluate --config config/rag_eval.yaml --limit 5
```

## 14. 风险与应对

### 14.1 LLM JSON 不稳定

应对：

- 强 prompt；
- code block JSON 提取；
- Pydantic 校验；
- 失败重试；
- raw response 落盘。

### 14.2 评测集偏置

应对：

- 多路候选证据池；
- 不直接使用线上 top-k 构造标准答案；
- human golden set；
- 区分 weak / golden 指标。

### 14.3 候选池过大导致成本高

应对：

- evidence card 压缩；
- max cards 限制；
- batch judging；
- `--limit` 调试；
- raw chunk 只在 synthesis 阶段少量传入。

### 14.4 chunk id 与现有索引不一致

应对：

- 优先读取现有索引产物；
- fallback 生成 chunk 时保持与 `DocumentSplitter` 一致；
- evaluate 阶段检测 stale evidence。

### 14.5 影响现有线上 RAG 链路

应对：

- 新功能放在 `src/evaluation/`；
- 新增独立 CLI；
- 不修改 `RAGPipeline` 主逻辑，除非后续明确重构。

## 15. 完成定义

### MVP 完成定义

- 可以生成至少 20 条候选问题。
- 可以构建候选证据池和 evidence cards。
- 可以调用 OpenAI-compatible API 生成 evidence judgments 和 eval dataset draft。
- 可以生成固定 `eval_dataset.jsonl`。
- 可以运行 retrieval-only 评测并输出 metrics/report。
- 每一步都可以单独执行。

### 完整版完成定义

- 支持人工审核导出与回填。
- 支持 weak / golden 数据集区分。
- 支持 LLM-as-Judge 生成质量评分。
- 支持 must-have / nice-to-have coverage。
- 支持多配置对比。
- 支持 hard negatives 和成本统计。

## 16. 下一步

完成本 workflow 后，下一步应使用 `/sc:implement` 或手动按 MVP 执行顺序开始实现。建议第一轮只实现 Phase 1-5，先保证小样本闭环可运行，再扩展审核、LLM-as-Judge 和多配置对比。
