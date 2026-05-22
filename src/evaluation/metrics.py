"""Metrics for retrieval-only RAG evaluation."""

from __future__ import annotations

import math
from statistics import mean


def evidence_hit_at_k(retrieved: list[str], acceptable: list[str], k: int) -> float:
    return 1.0 if set(retrieved[:k]) & set(acceptable) else 0.0


def evidence_recall_at_k(retrieved: list[str], acceptable: list[str], k: int) -> float:
    if not acceptable:
        return 0.0
    return len(set(retrieved[:k]) & set(acceptable)) / len(set(acceptable))


def mrr(retrieved: list[str], acceptable: list[str]) -> float:
    acceptable_set = set(acceptable)
    for index, chunk_id in enumerate(retrieved, start=1):
        if chunk_id in acceptable_set:
            return 1.0 / index
    return 0.0


def ndcg_at_k(retrieved: list[str], acceptable: list[str], k: int) -> float:
    acceptable_set = set(acceptable)
    if not acceptable_set:
        return 0.0
    dcg = 0.0
    for index, chunk_id in enumerate(retrieved[:k], start=1):
        if chunk_id in acceptable_set:
            dcg += 1.0 / math.log2(index + 1)
    ideal_count = min(len(acceptable_set), k)
    idcg = sum(1.0 / math.log2(index + 1) for index in range(1, ideal_count + 1))
    return dcg / idcg if idcg else 0.0


def summarize_results(results: list[dict], top_ks: list[int]) -> dict:
    if not results:
        return {"num_cases": 0, "retrieval": {}, "latency": {}}
    retrieval = {}
    for k in top_ks:
        retrieval[f"hit@{k}"] = mean(item["metrics"].get(f"hit@{k}", 0.0) for item in results)
        retrieval[f"recall@{k}"] = mean(item["metrics"].get(f"recall@{k}", 0.0) for item in results)
        retrieval[f"ndcg@{k}"] = mean(item["metrics"].get(f"ndcg@{k}", 0.0) for item in results)
    retrieval["mrr"] = mean(item["metrics"].get("mrr", 0.0) for item in results)
    return {
        "num_cases": len(results),
        "retrieval": retrieval,
        "latency": {
            "avg_retrieval_ms": mean(item.get("latency_ms", 0.0) for item in results),
        },
    }
