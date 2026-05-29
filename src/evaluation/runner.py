"""Run retrieval-only evaluation on finalized eval datasets."""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path

from src.core.config import get_settings
from src.pipeline.rag_pipeline import RAGPipeline

from .chunk_source import ChunkSource
from .config import RagEvalConfig
from .io import read_jsonl, write_jsonl
from .metrics import evidence_hit_at_k, evidence_recall_at_k, mrr, ndcg_at_k, summarize_results
from .schemas import EvalSample


class RetrievalEvaluationRunner:
    def __init__(self, config: RagEvalConfig):
        self.config = config
        self.settings = get_settings(config.paths.system_config)
        self.pipeline = RAGPipeline(self.settings)
        self.chunk_source = ChunkSource(config)

    def run(self, limit: int | None = None, offset: int = 0) -> Path:
        dataset_path = Path(self.config.evaluation.dataset_path)
        samples = read_jsonl(dataset_path, EvalSample)[offset:]
        if limit:
            samples = samples[:limit]
        run_dir = self.config.output_dir / "runs" / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        run_dir.mkdir(parents=True, exist_ok=True)
        results = []
        max_k = max(self.config.evaluation.top_k)
        for sample in samples:
            t0 = time.time()
            retrieved = self._retrieve(sample.question, max_k)
            latency_ms = (time.time() - t0) * 1000
            retrieved_ids = [item.chunk_id for item in retrieved]
            metric_retrieved_ids = self._canonicalize_ids(retrieved_ids)
            metric_acceptable_ids = self._canonicalize_ids(sample.acceptable_chunk_ids)
            metrics = {"mrr": mrr(metric_retrieved_ids, metric_acceptable_ids)}
            for k in self.config.evaluation.top_k:
                metrics[f"hit@{k}"] = evidence_hit_at_k(metric_retrieved_ids, metric_acceptable_ids, k)
                metrics[f"recall@{k}"] = evidence_recall_at_k(metric_retrieved_ids, metric_acceptable_ids, k)
                metrics[f"ndcg@{k}"] = ndcg_at_k(metric_retrieved_ids, metric_acceptable_ids, k)
            results.append({
                "sample_id": sample.id,
                "question": sample.question,
                "question_scope": sample.question_scope,
                "retrieved_ids": retrieved_ids,
                "acceptable_chunk_ids": sample.acceptable_chunk_ids,
                "metrics": metrics,
                "latency_ms": latency_ms,
            })
        write_jsonl(run_dir / "retrieval_results.jsonl", results)
        summary = summarize_results(results, self.config.evaluation.top_k)
        write_jsonl(run_dir / "metrics.jsonl", [summary])
        return run_dir

    def _canonicalize_ids(self, chunk_ids: list[str]) -> list[str]:
        canonical = []
        for chunk_id in chunk_ids:
            chunk = self.chunk_source.get(chunk_id)
            canonical.append(chunk.parent_id if chunk and chunk.parent_id else chunk_id)
        return canonical

    def _retrieve(self, question: str, k: int):
        query_embedding = self.pipeline.embedding_service.embed_query(question)
        results = self.pipeline.retriever.retrieve(question, query_embedding, k=k * 2)
        if self.settings.retrieval.rerank:
            results = self.pipeline.reranker.rerank(results, question)
        results = self.pipeline.kg_enhancer.enhance(results, question)
        return results[:k]
