"""
RAG System Evaluation Script

Evaluates retrieval quality, generation quality, and latency.

Usage:
    python scripts/evaluate.py --data scripts/eval_data_sample.json --top-k 5

Evaluation data format (JSON):
[
    {
        "question": "...",
        "ground_truth_answer": "...",
        "ground_truth_contexts": ["chunk_id_1", "chunk_id_2"],
        "question_type": "定位指导"  // optional
    }
]
"""

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import jieba
import numpy as np
from sentence_transformers import SentenceTransformer

from src.core.config import get_settings
from src.generation.llm_service import LLMService
from src.pipeline.rag_pipeline import RAGPipeline


# ─── Data Models ────────────────────────────────────────────────────────────


@dataclass
class EvalCase:
    """Single evaluation case"""
    question: str
    ground_truth_answer: str
    ground_truth_contexts: List[str]
    question_type: Optional[str] = None


@dataclass
class RetrievalMetrics:
    """Retrieval quality metrics for a single case"""
    recall_at_k: float = 0.0
    precision_at_k: float = 0.0
    mrr: float = 0.0
    ndcg_at_k: float = 0.0
    hit: bool = False


@dataclass
class GenerationMetrics:
    """Generation quality metrics"""
    # LLM-as-judge scores (1-5)
    faithfulness: float = 0.0
    relevance: float = 0.0
    correctness: float = 0.0
    completeness: float = 0.0
    # Non-LLM metrics (0-1)
    rouge_l: float = 0.0
    bert_score: float = 0.0
    keyword_coverage: float = 0.0


@dataclass
class LatencyMetrics:
    """Latency metrics in milliseconds"""
    first_token_ms: float = 0.0
    total_ms: float = 0.0


@dataclass
class CaseResult:
    """Evaluation result for a single case"""
    question: str
    answer: str
    retrieved_ids: List[str]
    retrieval: RetrievalMetrics = field(default_factory=RetrievalMetrics)
    generation: GenerationMetrics = field(default_factory=GenerationMetrics)
    latency: LatencyMetrics = field(default_factory=LatencyMetrics)
    judge_reasons: dict = field(default_factory=dict)


@dataclass
class EvalReport:
    """Aggregated evaluation report"""
    num_cases: int = 0
    top_k: int = 5
    cases: List[CaseResult] = field(default_factory=list)

    # Averaged metrics
    avg_recall: float = 0.0
    avg_precision: float = 0.0
    avg_mrr: float = 0.0
    avg_ndcg: float = 0.0
    hit_rate: float = 0.0
    avg_faithfulness: float = 0.0
    avg_relevance: float = 0.0
    avg_correctness: float = 0.0
    avg_completeness: float = 0.0
    avg_rouge_l: float = 0.0
    avg_bert_score: float = 0.0
    avg_keyword_coverage: float = 0.0
    avg_first_token_ms: float = 0.0
    avg_total_ms: float = 0.0


# ─── LLM Judge Prompts ─────────────────────────────────────────────────────

JUDGE_FAITHFULNESS = """你是一个忠实度评估专家。请评估以下回答是否忠于提供的检索文档，有无幻觉。

用户问题：{question}

检索到的文档：
{contexts}

AI回答：
{answer}

评分标准（1-5分）：
5分：回答中的所有信息都能在检索文档中找到依据
4分：绝大部分信息有依据，极少量推断合理
3分：大部分信息有依据，但有少量无依据的推断
2分：较多信息缺乏文档依据
1分：回答大部分是幻觉，与文档不符

请只返回JSON格式：{{"score": <1-5>, "reason": "<简要理由>"}}"""

JUDGE_RELEVANCE = """你是一个相关性评估专家。请评估以下回答是否切题，是否解答了用户的问题。

用户问题：{question}

AI回答：
{answer}

评分标准（1-5分）：
5分：完全切题，精准解答了用户问题
4分：基本切题，回答了主要问题
3分：部分切题，回答了一些相关内容但不够聚焦
2分：偏离主题，大部分内容不相关
1分：完全不相关

请只返回JSON格式：{{"score": <1-5>, "reason": "<简要理由>"}}"""

JUDGE_CORRECTNESS = """你是一个正确性评估专家。请评估以下回答与标准答案的语义一致性。

用户问题：{question}

标准答案：
{ground_truth}

AI回答：
{answer}

评分标准（1-5分）：
5分：回答与标准答案核心信息完全一致
4分：回答涵盖了标准答案的主要信息，表述略有差异
3分：回答涵盖了部分关键信息，有遗漏
2分：回答与标准答案有较大出入
1分：回答与标准答案完全不符

请只返回JSON格式：{{"score": <1-5>, "reason": "<简要理由>"}}"""

JUDGE_COMPLETENESS = """你是一个完整性评估专家。请评估以下回答是否覆盖了标准答案中的关键信息点。

用户问题：{question}

标准答案：
{ground_truth}

AI回答：
{answer}

评分标准（1-5分）：
5分：覆盖了标准答案中所有关键信息点
4分：覆盖了大部分关键信息点，遗漏1-2个次要信息
3分：覆盖了约一半的关键信息点
2分：仅覆盖了少量关键信息点
1分：几乎未覆盖关键信息点

请只返回JSON格式：{{"score": <1-5>, "reason": "<简要理由>"}}"""


# ─── Evaluator ──────────────────────────────────────────────────────────────


class RAGEvaluator:
    """RAG system evaluator"""

    # ── Retrieval Metrics ────────────────────────────────────────────────

    @staticmethod
    def calc_recall_at_k(retrieved: List[str], ground_truth: List[str], k: int) -> float:
        """Recall@K: proportion of ground truth found in top-k results"""
        if not ground_truth:
            return 1.0
        retrieved_at_k = set(retrieved[:k])
        hits = len(retrieved_at_k & set(ground_truth))
        return hits / len(ground_truth)

    @staticmethod
    def calc_precision_at_k(retrieved: List[str], ground_truth: List[str], k: int) -> float:
        """Precision@K: proportion of top-k results that are correct"""
        if k == 0:
            return 0.0
        retrieved_at_k = set(retrieved[:k])
        hits = len(retrieved_at_k & set(ground_truth))
        return hits / k

    @staticmethod
    def calc_mrr(retrieved: List[str], ground_truth: List[str]) -> float:
        """Mean Reciprocal Rank: 1/rank of first correct result"""
        gt_set = set(ground_truth)
        for i, doc_id in enumerate(retrieved):
            if doc_id in gt_set:
                return 1.0 / (i + 1)
        return 0.0

    @staticmethod
    def calc_ndcg_at_k(retrieved: List[str], ground_truth: List[str], k: int) -> float:
        """NDCG@K: Normalized Discounted Cumulative Gain"""
        gt_set = set(ground_truth)
        if not gt_set:
            return 1.0

        # DCG: sum of 1/log2(i+2) for relevant docs at position i
        dcg = 0.0
        for i, doc_id in enumerate(retrieved[:k]):
            if doc_id in gt_set:
                dcg += 1.0 / math.log2(i + 2)

        # Ideal DCG: all relevant docs at top positions
        ideal_k = min(len(gt_set), k)
        idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_k))

        return dcg / idcg if idcg > 0 else 0.0

    # ── Non-LLM Generation Metrics ──────────────────────────────────────

    def __init__(self, settings, pipeline: RAGPipeline, llm_judge: LLMService):
        self.pipeline = pipeline
        self.llm = llm_judge
        self.top_k = 5
        self._bert_model: Optional[SentenceTransformer] = None

    def _get_bert_model(self) -> SentenceTransformer:
        if self._bert_model is None:
            print("  Loading BERTScore model...")
            self._bert_model = SentenceTransformer("BAAI/bge-large-zh")
        return self._bert_model

    @staticmethod
    def calc_rouge_l(prediction: str, reference: str) -> float:
        """ROUGE-L score based on Longest Common Subsequence"""
        if not prediction or not reference:
            return 0.0

        # Tokenize with jieba for Chinese
        pred_tokens = list(jieba.cut(prediction))
        ref_tokens = list(jieba.cut(reference))

        m, n = len(pred_tokens), len(ref_tokens)
        if m == 0 or n == 0:
            return 0.0

        # LCS DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if pred_tokens[i - 1] == ref_tokens[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        lcs_len = dp[m][n]
        precision = lcs_len / m
        recall = lcs_len / n
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    def calc_bert_score(self, prediction: str, reference: str) -> float:
        """BERTScore: cosine similarity of sentence embeddings"""
        if not prediction or not reference:
            return 0.0
        model = self._get_bert_model()
        embeddings = model.encode([prediction, reference], normalize_embeddings=True)
        return float(np.dot(embeddings[0], embeddings[1]))

    @staticmethod
    def calc_keyword_coverage(prediction: str, reference: str) -> float:
        """Keyword coverage: proportion of reference keywords found in prediction"""
        if not reference:
            return 1.0

        ref_tokens = set(jieba.lcut(reference))
        pred_tokens = set(jieba.lcut(prediction))

        # Filter: keep tokens with len > 1 (skip single chars and punctuation)
        ref_keywords = {t for t in ref_tokens if len(t) > 1}
        if not ref_keywords:
            return 1.0

        pred_keywords = {t for t in pred_tokens if len(t) > 1}
        covered = ref_keywords & pred_keywords
        return len(covered) / len(ref_keywords)

    # ── LLM-as-Judge ────────────────────────────────────────────────────

    def _judge(self, prompt: str) -> tuple[float, str]:
        """Call LLM judge and parse score + reason"""
        try:
            response = self.llm.generate(prompt, temperature=0.0, max_tokens=200)
            # Parse JSON from response (handle markdown code blocks)
            text = response.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            data = json.loads(text)
            score = float(data.get("score", 0))
            reason = data.get("reason", "")
            return max(1.0, min(5.0, score)), reason
        except Exception as e:
            return 0.0, f"Judge error: {e}"

    def judge_faithfulness(self, question: str, answer: str, contexts: List[str]) -> tuple[float, str]:
        contexts_text = "\n---\n".join(contexts) if contexts else "(无文档)"
        prompt = JUDGE_FAITHFULNESS.format(question=question, answer=answer, contexts=contexts_text)
        return self._judge(prompt)

    def judge_relevance(self, question: str, answer: str) -> tuple[float, str]:
        prompt = JUDGE_RELEVANCE.format(question=question, answer=answer)
        return self._judge(prompt)

    def judge_correctness(self, question: str, answer: str, ground_truth: str) -> tuple[float, str]:
        prompt = JUDGE_CORRECTNESS.format(question=question, answer=answer, ground_truth=ground_truth)
        return self._judge(prompt)

    def judge_completeness(self, question: str, answer: str, ground_truth: str) -> tuple[float, str]:
        prompt = JUDGE_COMPLETENESS.format(question=question, answer=answer, ground_truth=ground_truth)
        return self._judge(prompt)

    # ── Single Case Evaluation ──────────────────────────────────────────

    def evaluate_case(self, case: EvalCase) -> CaseResult:
        """Evaluate a single question"""
        result = CaseResult(question=case.question, answer="", retrieved_ids=[])

        # 1. Run retrieval (without LLM generation)
        t0 = time.time()
        query_embedding = self.pipeline.embedding_service.embed_query(case.question)
        retrieval_results = self.pipeline.retriever.retrieve(
            query=case.question,
            query_embedding=query_embedding,
            k=self.top_k * 2,
        )
        if self.pipeline.settings.retrieval.rerank:
            retrieval_results = self.pipeline.reranker.rerank(retrieval_results, case.question)
        retrieval_results = retrieval_results[: self.top_k]

        result.retrieved_ids = [r.chunk_id for r in retrieval_results]
        retrieved_contents = [r.content for r in retrieval_results]

        # 2. Run full pipeline (with LLM generation) for latency and answer
        t_start = time.time()
        response = self.pipeline.query(case.question, top_k=self.top_k)
        t_end = time.time()

        result.answer = response.answer
        result.latency.total_ms = (t_end - t_start) * 1000

        # 3. Calculate retrieval metrics
        gt = case.ground_truth_contexts
        result.retrieval.recall_at_k = self.calc_recall_at_k(result.retrieved_ids, gt, self.top_k)
        result.retrieval.precision_at_k = self.calc_precision_at_k(result.retrieved_ids, gt, self.top_k)
        result.retrieval.mrr = self.calc_mrr(result.retrieved_ids, gt)
        result.retrieval.ndcg_at_k = self.calc_ndcg_at_k(result.retrieved_ids, gt, self.top_k)
        result.retrieval.hit = result.retrieval.recall_at_k > 0

        # 4. Non-LLM generation metrics (fast, no API call)
        result.generation.rouge_l = self.calc_rouge_l(result.answer, case.ground_truth_answer)
        result.generation.bert_score = self.calc_bert_score(result.answer, case.ground_truth_answer)
        result.generation.keyword_coverage = self.calc_keyword_coverage(result.answer, case.ground_truth_answer)

        # 5. LLM-as-judge generation metrics (slow, requires API call)
        score, reason = self.judge_faithfulness(case.question, result.answer, retrieved_contents)
        result.generation.faithfulness = score
        result.judge_reasons["faithfulness"] = reason

        score, reason = self.judge_relevance(case.question, result.answer)
        result.generation.relevance = score
        result.judge_reasons["relevance"] = reason

        score, reason = self.judge_correctness(case.question, result.answer, case.ground_truth_answer)
        result.generation.correctness = score
        result.judge_reasons["correctness"] = reason

        score, reason = self.judge_completeness(case.question, result.answer, case.ground_truth_answer)
        result.generation.completeness = score
        result.judge_reasons["completeness"] = reason

        return result

    # ── Full Evaluation ─────────────────────────────────────────────────

    def evaluate_dataset(self, dataset: List[EvalCase], top_k: int = 5) -> EvalReport:
        """Evaluate the full dataset"""
        self.top_k = top_k
        report = EvalReport(num_cases=len(dataset), top_k=top_k)

        for i, case in enumerate(dataset):
            print(f"\n[{i+1}/{len(dataset)}] {case.question}")
            result = self.evaluate_case(case)
            report.cases.append(result)

            r = result.retrieval
            g = result.generation
            print(f"  Retrieval  - Recall: {r.recall_at_k:.2f}  Precision: {r.precision_at_k:.2f}  "
                  f"MRR: {r.mrr:.2f}  NDCG: {r.ndcg_at_k:.2f}  Hit: {r.hit}")
            print(f"  Auto Metrics  - ROUGE-L: {g.rouge_l:.3f}  BERTScore: {g.bert_score:.3f}  "
                  f"KW-Coverage: {g.keyword_coverage:.3f}")
            print(f"  LLM Judge  - Faith: {g.faithfulness:.1f}  Rel: {g.relevance:.1f}  "
                  f"Corr: {g.correctness:.1f}  Comp: {g.completeness:.1f}")
            print(f"  Latency    - {result.latency.total_ms:.0f}ms")

        # Aggregate
        n = len(report.cases) or 1
        report.avg_recall = sum(c.retrieval.recall_at_k for c in report.cases) / n
        report.avg_precision = sum(c.retrieval.precision_at_k for c in report.cases) / n
        report.avg_mrr = sum(c.retrieval.mrr for c in report.cases) / n
        report.avg_ndcg = sum(c.retrieval.ndcg_at_k for c in report.cases) / n
        report.hit_rate = sum(1 for c in report.cases if c.retrieval.hit) / n
        report.avg_faithfulness = sum(c.generation.faithfulness for c in report.cases) / n
        report.avg_relevance = sum(c.generation.relevance for c in report.cases) / n
        report.avg_correctness = sum(c.generation.correctness for c in report.cases) / n
        report.avg_completeness = sum(c.generation.completeness for c in report.cases) / n
        report.avg_rouge_l = sum(c.generation.rouge_l for c in report.cases) / n
        report.avg_bert_score = sum(c.generation.bert_score for c in report.cases) / n
        report.avg_keyword_coverage = sum(c.generation.keyword_coverage for c in report.cases) / n
        report.avg_first_token_ms = sum(c.latency.first_token_ms for c in report.cases) / n
        report.avg_total_ms = sum(c.latency.total_ms for c in report.cases) / n

        return report

    # ── Report ──────────────────────────────────────────────────────────

    @staticmethod
    def print_report(report: EvalReport):
        """Print evaluation report to terminal"""
        print("\n" + "=" * 60)
        print("  RAG Evaluation Report")
        print("=" * 60)
        print(f"  Cases: {report.num_cases}    Top-K: {report.top_k}")
        print("-" * 60)

        print("\n  Retrieval Metrics:")
        print(f"    Recall@{report.top_k}     : {report.avg_recall:.4f}")
        print(f"    Precision@{report.top_k}  : {report.avg_precision:.4f}")
        print(f"    MRR            : {report.avg_mrr:.4f}")
        print(f"    NDCG@{report.top_k}      : {report.avg_ndcg:.4f}")
        print(f"    Hit Rate       : {report.hit_rate:.4f}")

        print("\n  Auto Metrics (no LLM, 0-1):")
        print(f"    ROUGE-L        : {report.avg_rouge_l:.4f}")
        print(f"    BERTScore      : {report.avg_bert_score:.4f}")
        print(f"    KW-Coverage    : {report.avg_keyword_coverage:.4f}")

        print("\n  Generation Metrics (LLM-as-judge, 1-5):")
        print(f"    Faithfulness   : {report.avg_faithfulness:.2f}")
        print(f"    Relevance      : {report.avg_relevance:.2f}")
        print(f"    Correctness    : {report.avg_correctness:.2f}")
        print(f"    Completeness   : {report.avg_completeness:.2f}")

        print("\n  Latency:")
        print(f"    Avg Total      : {report.avg_total_ms:.0f}ms")

        print("\n  Per-case Details:")
        print("-" * 60)
        for i, c in enumerate(report.cases):
            r = c.retrieval
            g = c.generation
            print(f"  [{i+1}] {c.question[:40]}...")
            print(f"      Recall={r.recall_at_k:.2f}  MRR={r.mrr:.2f}  "
                  f"ROUGE-L={g.rouge_l:.3f}  BERT={g.bert_score:.3f}  KW={g.keyword_coverage:.3f}")
            print(f"      Faith={g.faithfulness:.1f}  Rel={g.relevance:.1f}  "
                  f"Corr={g.correctness:.1f}  Comp={g.completeness:.1f}  "
                  f"{c.latency.total_ms:.0f}ms")
            if c.judge_reasons:
                for metric, reason in c.judge_reasons.items():
                    if reason:
                        print(f"      {metric}: {reason[:60]}")

        print("=" * 60)

    @staticmethod
    def save_report(report: EvalReport, output_path: str):
        """Save report as JSON"""
        data = {
            "summary": {
                "num_cases": report.num_cases,
                "top_k": report.top_k,
                "retrieval": {
                    "recall": round(report.avg_recall, 4),
                    "precision": round(report.avg_precision, 4),
                    "mrr": round(report.avg_mrr, 4),
                    "ndcg": round(report.avg_ndcg, 4),
                    "hit_rate": round(report.hit_rate, 4),
                },
                "generation": {
                    "faithfulness": round(report.avg_faithfulness, 2),
                    "relevance": round(report.avg_relevance, 2),
                    "correctness": round(report.avg_correctness, 2),
                    "completeness": round(report.avg_completeness, 2),
                },
                "auto_metrics": {
                    "rouge_l": round(report.avg_rouge_l, 4),
                    "bert_score": round(report.avg_bert_score, 4),
                    "keyword_coverage": round(report.avg_keyword_coverage, 4),
                },
                "latency": {
                    "avg_total_ms": round(report.avg_total_ms, 0),
                },
            },
            "cases": [],
        }

        for c in report.cases:
            data["cases"].append({
                "question": c.question,
                "answer": c.answer,
                "retrieved_ids": c.retrieved_ids,
                "retrieval": {
                    "recall": round(c.retrieval.recall_at_k, 4),
                    "precision": round(c.retrieval.precision_at_k, 4),
                    "mrr": round(c.retrieval.mrr, 4),
                    "ndcg": round(c.retrieval.ndcg_at_k, 4),
                    "hit": c.retrieval.hit,
                },
                "generation": {
                    "faithfulness": round(c.generation.faithfulness, 2),
                    "relevance": round(c.generation.relevance, 2),
                    "correctness": round(c.generation.correctness, 2),
                    "completeness": round(c.generation.completeness, 2),
                },
                "auto_metrics": {
                    "rouge_l": round(c.generation.rouge_l, 4),
                    "bert_score": round(c.generation.bert_score, 4),
                    "keyword_coverage": round(c.generation.keyword_coverage, 4),
                },
                "judge_reasons": c.judge_reasons,
                "latency_ms": round(c.latency.total_ms, 0),
            })

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nReport saved to: {output_path}")


# ─── Main ───────────────────────────────────────────────────────────────────


def load_dataset(path: str) -> List[EvalCase]:
    """Load evaluation dataset from JSON file"""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    cases = []
    for item in data:
        cases.append(EvalCase(
            question=item["question"],
            ground_truth_answer=item.get("ground_truth_answer", ""),
            ground_truth_contexts=item.get("ground_truth_contexts", []),
            question_type=item.get("question_type"),
        ))
    return cases


def main():
    parser = argparse.ArgumentParser(description="RAG System Evaluation")
    parser.add_argument("--data", required=True, help="Path to evaluation dataset JSON")
    parser.add_argument("--top-k", type=int, default=5, help="Top-K for retrieval")
    parser.add_argument("--output", default=None, help="Output report path (default: eval_report_<timestamp>.json)")
    parser.add_argument("--config", default=None, help="Config file path")
    args = parser.parse_args()

    # Load config
    settings = get_settings(args.config) if args.config else get_settings()

    # Initialize pipeline
    print("Initializing RAG pipeline...")
    pipeline = RAGPipeline(settings)

    # Initialize LLM judge
    print("Initializing LLM judge...")
    api_key = settings.get_llm_api_key()
    llm_judge = LLMService(
        provider=settings.llm.provider,
        api_key=api_key,
        model=settings.llm.model,
        base_url=settings.llm.base_url,
        max_tokens=settings.llm.max_tokens,
        temperature=0.0,
    )

    # Load dataset
    print(f"Loading dataset from {args.data}...")
    dataset = load_dataset(args.data)
    print(f"Loaded {len(dataset)} evaluation cases")

    # Run evaluation
    evaluator = RAGEvaluator(settings, pipeline, llm_judge)
    report = evaluator.evaluate_dataset(dataset, top_k=args.top_k)

    # Print report
    evaluator.print_report(report)

    # Save report
    output_path = args.output or f"eval_report_{int(time.time())}.json"
    evaluator.save_report(report, output_path)


if __name__ == "__main__":
    main()
